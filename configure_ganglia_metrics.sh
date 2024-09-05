#!/bin/bash
source ./env.sh

if [[ ! -d $LOGS_DIR ]] ; then
    sudo mkdir -p $LOGS_DIR
fi

STOP_FILE="$LOGS_DIR/stop_signal"
if ! grep -q "alias stop-gangliaMetrics=" ~/.bashrc; then
     echo alias stop-gangliaMetrics="'touch $STOP_FILE'" >> ~/.bashrc
fi

if [[ $GANGLIA_METRICS_ENABLED != "true" ]]; then
    echo "Ganglia metrics on $GANGLIA_METRICS_CLUSTER_NAME are not enabled"
    exit 0
fi

echo "Enabling collection of metrics on $GANGLIA_METRICS_CLUSTER_NAME"
cp ./env.sh /tmp/env.sh
chmod a+x /tmp/env.sh

GATHER_SCRIPT="/tmp/gather_ganglia_metrics.sh"

if [[ -f $GATHER_SCRIPT ]]; then
    echo "The gather_ganglia_metrics.sh script already exists. Skipping creation."
else
    cat <<'EOF' >> $GATHER_SCRIPT
#!/bin/bash

# Assign poll interval
source /tmp/env.sh

STOP_FILE="$LOGS_DIR/stop_signal"

if [[ -z "$LOGS_DIR" || ! -d "$LOGS_DIR" ]]; then
    echo "Error: The LOGS_DIR directory is not defined or does not exist."
    exit 1
fi

if [[ -z "$STOP_FILE" ]]; then
    echo "Error: The STOP_FILE variable is not correctly defined."
    exit 1
fi

re='^[0-9]+$'
if [[ $GANGLIA_METRICS_POLL_INTERVAL =~ $re ]] ; then
    POLL_INTERVAL=$GANGLIA_METRICS_POLL_INTERVAL
else
    POLL_INTERVAL="60"
fi
while true; do
    # Check if the stop signal file exists
    if [[ -f $STOP_FILE ]]; then
        echo "Stop signal detected. Executing final cleanup command"
        rm "$LOGS_DIR"/*
        rm -f $STOP_FILE # Remove the stop signal file after use
        exit 0
    fi
    rm "$LOGS_DIR"/* 2> /dev/null
    LOG_TIMESTAMP=$(date '+%Y%m%d%H%M%S')
    LOG_PATH="$LOGS_DIR/$LOG_TIMESTAMP.xml"
    curl -s http://"$GANGLIA_IP":8652/"$GANGLIA_METRICS_CLUSTER_NAME"/*/{cpu_system,cpu_idle,cpu_user} >> $LOG_PATH
    python3 xmlToCsv.py --path "$LOG_PATH"
    python3 sendCsvToDruid.py
    sleep $POLL_INTERVAL
done
EOF
    chmod a+x $GATHER_SCRIPT
fi

$GATHER_SCRIPT & disown
