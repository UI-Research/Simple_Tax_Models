#!/bin/bash

# install python 3 and necessary libraries
sudo yum update -y
sudo yum install -y python36 python36-pip
sudo python3 -m pip install requests

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

# copy rancher-compose python script and supporting files from s3
sudo aws s3 cp s3://your_bucket/run-rancher-compose.py /usr/local/sbin/run-rancher-compose.py
sudo aws s3 cp s3://your_bucket/simple-tax-model/docker-compose-job-submitter-template.yml /usr/local/sbin/docker-compose-job-submitter-template.yml
sudo aws s3 cp s3://your_bucket/simple-tax-model/rancher-compose.yml /usr/local/sbin/rancher-compose.yml
sudo aws s3 cp s3://your_bucket/simple-tax-model/credentials.py /usr/local/sbin/credentials.py

# create empty docker-compose file with correct permissions
sudo touch /usr/local/sbin/docker-compose-job-submitter.yml
sudo chmod 777 /usr/local/sbin/docker-compose-job-submitter.yml
