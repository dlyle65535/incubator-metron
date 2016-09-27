#!/bin/bash

PASSWORD=admin
CLUSTER_NAME=metron_cluster
METRON_DIR=/usr/metron/0.2.0BETA
METRON_SRC=/root/metron/metron-platform
METRON_FILES=/root/metron/scripts

#echo "I'm doing it!"
#touch /tmp/ididit
while ! nc -z localhost 8080; do sleep 0.1; done; echo 'Ambari Server server is UP'

echo "Stopping Monit"
service monit stop


#- include: topologies.yml
#
#- include: source_config.yml
#  run_once: true
#
#- include: threat_intel.yml
#  run_once: true
#  when: threat_intel_bulk_load == True
#
#- include: hdfs_purge.yml
#
#- include: es_purge.yml

echo "Unpack Metron Bundles"
mkdir -p $METRON_DIR
cd $METRON_DIR
tar xzvf $METRON_SRC/metron-elasticsearch/target/metron-elasticsearch*.tar.gz
tar xzvf $METRON_SRC/metron-enrichment/target/metron-enrichment*.tar.gz
tar xzvf $METRON_SRC/metron-indexing/target/metron-indexing*.tar.gz
tar xzvf $METRON_SRC/metron-parsers/target/metron-parsers*.tar.gz
tar xzvf $METRON_SRC/metron-data-management/target/metron-data-management*.tar.gz
tar xzvf $METRON_SRC/metron-common/target/metron-common*.tar.gz

echo "Setup Config"
cp /root/metron/scripts/enrichment.properties $METRON_DIR/config/.

echo "Waiting 2 minutes for ambari-agent"
#sleep 120

echo "Starting HDP"
curl -sS -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start all Services via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://`hostname -f`:8080/api/v1/clusters/$CLUSTER_NAME/services

#TODO - make this read ambari for status
echo "Waiting 2 minutes for Services to Start"
#sleep 120

echo "Setup HDFS for Metron"
sudo -H -u hdfs bash -c "hdfs dfs -mkdir -p /user/root"
sudo -H -u hdfs bash -c "hdfs dfs -chown root:root /user/root"
sudo -H -u hdfs bash -c "hdfs dfs -mkdir -p /apps/metron"
sudo -H -u hdfs bash -c "hdfs dfs -chown hdfs:hadoop /apps/metron"
sudo -H -u hdfs bash -c "hdfs dfs -chmod 775 /apps/metron"

echo "Upload Grok Patterns to HDFS"
sudo -H -u hdfs bash -c "hdfs dfs -mkdir -p /apps/metron/patterns"
sudo -H -u hdfs bash -c "hdfs dfs -chown -R hdfs:hadoop /apps/metron/patterns"
sudo -H -u hdfs bash -c "hdfs dfs -chmod -R 775 /apps/metron/patterns"
sudo -H -u hdfs bash -c "hdfs dfs -put -f $METRON_DIR/patterns  /apps/metron/"

echo $(pwd)
echo "Uploading configs to Zookeeper"
cp $METRON_FILES/global.json $METRON_DIR/config/zookeeper
$METRON_DIR/bin/zk_load_configs.sh --mode PUSH -i $METRON_DIR/config/zookeeper -z node1:2181
$METRON_DIR/bin/zk_load_configs.sh --mode DUMP -z node1:2181

echo "Starting Monit"
service monit start
