import os
import subprocess
import requests
import json

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
druid_ip = os.getenv('DRUID_IP')
druid_port = os.getenv('DRUID_PORT')
logs_dir = os.getenv('LOGS_DIR')

# Druid API URL, with f-string to insert the variables
url = f"http://{druid_ip}:{druid_port}/druid/indexer/v1/task"

def main():

    # Configuration of the ingestion task
    ingestion_task = {
        "type": "index_parallel",
        "spec": {
            "dataSchema": {
                "dataSource": "GangliaMetric",
                "timestampSpec": {
                    "column": "timestamp",
                    "format": "auto"
                },
                "dimensionsSpec": {
                    "dimensions": [
                        "version", "component", "url", "cluster", "host",
                        "ip", "metric", "unit", "description", "title"
                    ]
                },
                "metricsSpec": [
                    {
                        "name": "value",
                        "type": "doubleSum",
                        "fieldName": "value"
                    }
                ],
                "granularitySpec": {
                    "type": "uniform",
                    "segmentGranularity": "day",
                    "queryGranularity": "none",
                },
            },
            "ioConfig": {
                "type": "index_parallel",
                "appendToExisting": True,
                "inputSource": {
                    "type": "local",
                    "baseDir": logs_dir,
                    "filter": "*.csv"
                },
                "inputFormat": {
                    "type": "csv",
                    "findColumnsFromHeader": True,
                    "columns": [
                        "version", "component", "url", "timestamp", "cluster",
                        "host", "ip", "metric", "value", "unit", "description", "title"
                    ]
                }
            }
        }
    }

    # Sending the request to the Druid API
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(ingestion_task))

    # Checking the response
    if response.status_code != 200:
        print(f"Error while inserting the data:: {response.text}")

if __name__ == "__main__":
    main()
