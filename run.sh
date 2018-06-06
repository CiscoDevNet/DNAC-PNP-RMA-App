#!/bin/bash
echo Cluster IP : $CLUSTER_IP
echo Username   : $USERNAME
echo Password   : $PASSWORD

echo Default Device SSH Credentials
echo Username          : $DEVICE_USERNAME
echo Password          : $DEVICE_PASSWORD
echo Enable Password   : $DEVICE_ENABLE_PASSWORD


sed  -ie "s/{IP_ADDRESS}/$CLUSTER_IP/g" pnprma/conf/inputs.json
sed  -ie "s/{USERNAME}/$USERNAME/g" pnprma/conf/inputs.json
sed  -ie "s/{PASSWORD}/$PASSWORD/g" pnprma/conf/inputs.json

cd /home/pnprma/rma-ui/dna-app
nohup npm start > output.log&
cd /home/pnprma

echo "================================================================"
echo "================Access RMA UI http://localhost:3000 ============"
echo "================================================================"
python pnprma/app.py