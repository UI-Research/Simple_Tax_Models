#!/bin/bash

# install python 3 and necessary libraries
sudo yum update -y
sudo yum install -y python36 python36-pip
sudo python3 -m pip install requests
sudo python3 -m pip install pymysql

# install rancher-compose
# script via https://gist.github.com/jeefy/7fed19a335d5caae24639e7ee7be1b71
VERSION_NUM="0.12.5"
wget https://github.com/rancher/rancher-compose/releases/download/v0.12.5/rancher-compose-linux-amd64-v0.12.5.tar.gz
tar zxf rancher-compose-linux-amd64-v0.12.5.tar.gz
rm rancher-compose-linux-amd64-v0.12.5.tar.gz
sudo mv rancher-compose-v0.12.5/rancher-compose /usr/local/sbin/rancher-compose
sudo chmod +x /usr/local/sbin/rancher-compose
#sudo mv rancher-compose-v0.12.5/rancher-compose /usr/local/bin/rancher-compose
#sudo chmod +x /usr/local/bin/rancher-compose
rm -r rancher-compose-v0.12.5
