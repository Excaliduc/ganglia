import csv
import xml.etree.ElementTree as ET
import argparse
import os
import subprocess


def load_bash_env(file_path):
    command = f"bash -c 'source {file_path} && env'"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    output, _ = proc.communicate()
    
    env_vars = {}
    for line in output.decode('utf-8').splitlines():
        key, _, value = line.partition("=")
        env_vars[key] = value

    return env_vars

env_vars = load_bash_env('/tmp/env.sh')
os.environ.update(env_vars)
logs_dir = os.getenv('LOGS_DIR')

def split_xml_documents(xml_file):
    with open(xml_file, 'r') as file:
        content = file.read()
    documents = content.split('<?xml')
    documents = ['<?xml' + doc for doc in documents if doc.strip()]

    return documents

def parse_xml_to_csv(xml_content, csv_directory, file_prefix):
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Extract common details
    version = root.attrib.get('VERSION', 'Unknown')
    source = root.attrib.get('SOURCE', 'Unknown')
    authority = root.find('GRID').attrib.get('AUTHORITY', 'Unknown')
    timestamp = root.find('GRID').attrib.get('LOCALTIME', 'Unknown')
    cluster_name = root.find('GRID/CLUSTER').attrib.get('NAME', 'Unknown')

    # Iterate through the XML and extract the data
    for grid in root.findall('GRID'):
        for cluster in grid.findall('CLUSTER'):
            for host in cluster.findall('HOST'):
                host_name = host.get('NAME')
                host_ip = host.get('IP')
                for metric in host.findall('METRIC'):
                    metric_name = metric.get('NAME')
                    metric_val = metric.get('VAL')
                    metric_units = metric.get('UNITS')
                    metric_type = metric.get('TYPE')
                    extra_data = metric.find('EXTRA_DATA')
                    if extra_data is not None:
                        group = extra_data.find('EXTRA_ELEMENT[@NAME="GROUP"]').get('VAL')
                        description = extra_data.find('EXTRA_ELEMENT[@NAME="DESC"]').get('VAL')
                        title = extra_data.find('EXTRA_ELEMENT[@NAME="TITLE"]').get('VAL')
                    else:
                        group = description = title = ''

                    # Determine the CSV file path with the file_prefix
                    csv_file_path = os.path.join(csv_directory, f'{file_prefix}_{metric_name}.csv')

                    # Write to the corresponding CSV file
                    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        # Write the header if the file is new
                        if csv_file.tell() == 0:
                            header = ['version', 'component', 'url', 'timestamp', 'cluster', 'host', 'ip', 'metric', 'value', 'unit', 'description', 'title']
                            csv_writer.writerow(header)

                        row = [version, source, authority, timestamp, cluster_name, host_name, host_ip, metric_name, metric_val, metric_units, description, title]
                        csv_writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='Convert XML to CSV.')
    parser.add_argument('--path', type=str, help='Path to the XML file', required=True)    
    args = parser.parse_args()
    xml_file = args.path

    # Extract the base name of the XML file to use as a prefix
    file_prefix = os.path.splitext(os.path.basename(xml_file))[0]

    xml_documents = split_xml_documents(xml_file)

    for xml_content in xml_documents:
        parse_xml_to_csv(xml_content, logs_dir, file_prefix)

if __name__ == "__main__":
    main()
