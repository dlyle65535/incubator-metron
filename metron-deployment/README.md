# Overview
This set of playbooks can be used to deploy an Ambari-managed Hadoop cluster, Metron services, or both using ansible
playbooks. These playbooks currently only target RHEL/CentOS 6.x operating
systems.

## Prerequisites
The following tools are required to run these scripts:

- Maven - https://maven.apache.org/
- Git - https://git-scm.com/
- Ansible - http://www.ansible.com/ (version 2.0 or greater)

Currently Metron must be built from source.  Before running these scripts perform the following steps:

1. Clone the Metron git repository with `git clone git@github.com:apache/incubator-metron.git`
2. Navigate to `incubator-metron` and run `mvn clean package`

These scripts depend on two files for configuration:

- hosts - declares which Ansible roles will be run on which hosts
- group_vars/all - various configuration settings needed to install Metron

Examples can be found in the
`incubator-metron/metron-deployment/inventory/metron_example` directory and are a good starting point.  Copy this directory
into `incubator-metron/metron-deployment/inventory/` and rename it to your `project_name`.  More information about Ansible files and directory
structure can be found at http://docs.ansible.com/ansible/playbooks_best_practices.html.

## Ambari
The Ambari playbook will install a Hadoop cluster with all the services and configuration required by Metron.  This
section can be skipped if installing Metron on a pre-existing cluster.  

Currently, this playbook supports building a local development cluster running on one node but options for other types
 of clusters will be added in the future.

### Setting up your inventory
Make sure to update the hosts file in `incubator-metron/metron-deployment/inventory/project_name/hosts` or provide an
alternate inventory file when you launch the playbooks, including the
ssh user(s) and ssh keyfile location(s). These playbooks expect two
host groups:

- ambari_master
- ambari_slaves

### Running the playbook
This playbook will install the Ambari server on the ambari_master, install the ambari agents on
the ambari_slaves, and create a cluster in Ambari with a blueprint for the required
Metron components.

Navigate to `incubator-metron/metron-deployment/playbooks` and run:
`ansible-playbook -i ../inventory/project_name ambari_install.yml`

## Metron
The Metron playbook will gather the necessary cluster settings from Ambari and install the Metron services.

### Setting up your inventory
Edit the hosts file at `incubator-metron/metron-deployment/inventory/project_name/hosts`.  Declare where the
Metron services will be installed by updating these groups:

- [ambari_master] - host running Ambari
- ]ambari_slaves] - all Ambari-managed hosts
- [metron_kafka_topics] - host used to create the Kafka topics required by Metron. Requires a Kafka broker.
- [meron_hbase_tables] - host used to create the HBase tables required by Metron. Requires a HBase client.
- [enrichment] - submits the topology code to Storm and requires a Storm client
- [search] - host(s) where Elasticsearch will be installed
- [web] - host where the Metron UI and underlying services will be installed
- [sensors] - host where network data will be collected and published to Kafka

### Configuring group variables
The Metron Ansible scripts depend on a set of variables.  These variables can be found in the file at
`incubator-metron/metron-deployment/inventory/project_name/group_vars/all`.  

These variables are used to the deployment scripts to conform to your environment - look them over carefully. The most common changes are (defaults in italics):

**Ansible**
  - ansible_ssh_private_key_file: _/Path/to/private/key/file_ **Point to the private key file for ssh user on the target hosts**
  - ansible_ssh_user: _root_ **The name of the ssh user on the target hosts (requires sudo)**
  
**Ambari**
  - ambari_port: _8080_ **Change if your Ambari instance uses a non-default port**
  - ambari_user: _admin_ **Change to user on your Ambari instance**
  - ambari_password: _admin_ **Change to password for your Ambari user above**
 
**Kafka**
  - num_partitions: _3_ **Change to your desired number of partitions**
  - retention_in_gb: _25_ **Change to your desired retention size**
 
**Metron**
  - java_home: _/usr/jdk64/jdk1.8.0_40_ **Location of Java on all hosts**
  
**Sensors**
  - sensor_test_mode: _True_ **Change to false if not running traffic replay**
  - sniff_interface: _eth0_ **Interface that the Metron sensors will sniff on the [sensors] host**

**Search**
  - elasticsearch_network_interface: _eth0_ **Bind inteface for the Elasticsearch host(s)**
  
### Running the playbook
Navigate to `incubator-metron/metron-deployment/playbooks` and run:
`ansible-playbook -i ../inventory/project_name metron_install.yml --skip-tags="solr"`

## Vagrant
A VagrantFile is included and will install a working version of the entire Metron stack.  The following is required to
run this:

- Vagrant - https://www.vagrantup.com/
- Hostmanager plugin for vagrant - Run `vagrant plugin install vagrant-hostmanager` on the machine where Vagrant is
installed

Navigate to `incubator-metron/metron-deployment/vagrant/full-dev-platform` and run `vagrant up`.  This also provides a good
example of how to run a full end-to-end Metron install.


## TODO
- Support Ubuntu deployments
