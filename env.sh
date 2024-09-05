# env.sh

# example 
# export GANGLIA_METRICS_CLUSTER_NAME="MyCluster"
# export GANGLIA_METRICS_ENABLED="true"
# export GANGLIA_METRICS_POLL_INTERVAL="30"
# export GANGLIA_IP="localhost"
# export GANGLIA_PORT="8652"
# export ROOT_PATH="/var/log/ganglia_metrics/in"
# export DRUID_IP="localhost"
# export DRUID_PORT="8081"


export GANGLIA_METRICS_ENABLED="true"
export GANGLIA_METRICS_CLUSTER_NAME="Monstropolis"
export GANGLIA_METRICS_POLL_INTERVAL="30"
export GANGLIA_IP="localhost"
export GANGLIA_PORT="8652"
export ROOT_PATH="/var/log/ganglia_metrics/in"
export DRUID_IP="localhost"
export DRUID_PORT="8081"
export LOGS_DIR="$ROOT_PATH/$GANGLIA_METRICS_CLUSTER_NAME"

# export GANGLIA_METRICS_ENABLED="<true or false>""
# export GANGLIA_METRICS_CLUSTER_NAME="<name of your cluster"
# export GANGLIA_METRICS_POLL_INTERVAL="<time in seconde>"
# export GANGLIA_IP="<ganglia IP>"
# export GANGLIA_PORT="<ganglia port by defaul 8652>"
# export ROOT_PATH="<path for the xml and csv files>"
# export DRUID_IP="<druid IP>"
# export DRUID_PORT="<druid port by defaul 8081>"

