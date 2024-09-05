# Ganglia Exporter

## Introduction

The **Ganglia Exporter** is a suite of scripts designed to automate the collection, transformation, and ingestion of Ganglia metrics into an Apache Druid database for advanced analysis. This workflow enables the systematic export of Ganglia monitoring data, facilitating deeper insights through Apache Druid's powerful analytics capabilities.

## Prerequisites

Before you begin, ensure that the following prerequisites are met:

- **Apache Druid**: A fully configured and running Apache Druid instance accessible via a specified URL (*see details in the Annex*).
- **Python 3**: Installed with the necessary libraries, including **requests** for HTTP requests and **xml.etree.ElementTree** for XML parsing.
- **Ganglia**: Must be properly installed and operational, with metrics accessible via the Ganglia web interface.

## Installation

Follow these steps to install and configure the Ganglia Exporter:

### 1. Clone the Project

First, clone the project repository to your local machine:

```bash
git clone <repository-url>
cd <cloned-directory>
```

### 2. Configure Environment Variables

Edit the `env.sh` file to set the necessary environment variables, such as paths, IP addresses, and other configuration parameters. Use the example provided in the file as a template.

### 3. Grant Execution Rights

Ensure that the Bash scripts are executable. Run the following commands:

```bash
chmod +x configure_ganglia_metrics.sh
chmod +x env.sh
```

## Functionality

The Ganglia Exporter operates through a series of coordinated scripts, each responsible for a different part of the data collection and ingestion process:

### 1. Data Collection

The main Bash script (`configure_ganglia_metrics.sh`) interacts with the Ganglia API to fetch metrics related to `cpu_system`, `cpu_idle`, and `cpu_user` for all monitored hosts. The data is retrieved in XML format.

### 2. Data Transformation

The `xmlToCsv.py` script processes the collected XML data, converting it into CSV files. Each metric is saved in a separate CSV file, making the data easier to ingest into Apache Druid.

### 3. Data Ingestion

The `sendToDruid.py` script sends the CSV files to Apache Druid, where they are ingested for further analysis. This script handles the communication with Druid’s ingestion API, ensuring that the data is properly formatted and stored.

## Usage

### 1. Start Required Services

Before running the exporter, ensure all required services are up and running:

- **Ganglia** (frontend):
  
  ```bash
  systemctl start gmetad.service
  ```

- **Ganglia** (nodes):
  
  ```bash
  systemctl start gmond.service
  ```

- **Apache Druid**:
  
  ```bash
  ./<apache-druid-directory>/bin/start-druid
  ```

- **Grafana**:
  
  ```bash
  systemctl start grafana.service
  ```

### 2. Execute the Exporter Script

To begin exporting metrics, run the main exporter script:

```bash
./configure_ganglia_metrics.sh
```

This script initiates the data collection, transformation, and ingestion processes.

## Annex

### Port List

The following ports are used by the services involved in this workflow:

- **Apache Druid**: `8082`
- **Ganglia Web**: `8652`
- **Ganglia Exporter**: `8653`
- **Grafana**: `3000`

### Apache Druid Installation

If Apache Druid is not yet installed, follow these steps:

#### 1. Download the Apache Druid Archive

Download the `.tar.gz` file from the Apache website:

```bash
wget https://dlcdn.apache.org/druid/30.0.0/apache-druid-30.0.0-bin.tar.gz
```

#### 2. Extract the Archive

Extract the downloaded file and navigate to the extracted directory:

```bash
tar -xzf apache-druid-30.0.0-bin.tar.gz
cd apache-druid-30.0.0
```

#### 3. Start Apache Druid

Start the Apache Druid services using the following command:

```bash
./<apache-druid-directory>/bin/start-druid
```

### Frontend URL

To access the frontend for Ganglia or Druid, navigate to the appropriate URLs in your web browser. Replace `<hostname>` with the actual hostname or IP address of your server:

- **Ganglia**: `http://<hostname>:8652`
- **Apache Druid**: `http://<hostname>:8082`
- **Grafana**: `http://<hostname>:3000`
