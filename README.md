# DNAC-PNP RMA App

## Description
**DNAC-PNP RMA App** helps in restoring the configuration from faulty/old Cisco devices with newly shipped device. Post RMA the new device would have the exact same configuration as the faulty/old device.

### RMA Process
1. Device connects(ssh) to the faulty/old device
2. Fetches the config the device
3. Replace the old device with the new device
4. New device calls home to DNAC, which is picked up by PNP
5. Accept EULA on the new device
6. Reload the device
7. Push the config fetched from the faulty/old device to the new device
8. Once provisioned the new device would have the same configuration as the faulty/old device


### Assumptions
* The faulty/old device to be RMA’d is accessible via SSH, to get the Config from the device (Wouldn’t be able to retrieve the config when the device is totally down)
* The new device is exact same device as the old device, not all the commands are supported on different pids.

## Run from Docker
Run docker container with input parameters
- **docker run -p3000:3000 -p7001:7001  -e CLUSTER_IP="172.23.165.111" -e USERNAME="admin" -e PASSWORD="abc123"  ciscopnp/rmaapp**

- **args**
    -   CLUSTER_IP              =>  DNAC Cluster IP
    -   USERNAME                =>  DNAC Username
    -   PASSWORD                =>  DNAC Password

## Install and run locally  (Ignore if using PNP RMA App in docker)
1. Clone the repo from https://wwwin-github.cisco.com/pnp/appdev
2. In Terminal 1,
    -   Navigate to **appdev** directory
    -   Update conf/inputs.json, with DNAC Credentials, DNAC IP Address
    ![inputs.json](https://github.com/CiscoDevNet/DNAC-PNP-RMA-App/raw/ReadmeImageURL/images/input.jpg)
    -   Navigate back to **appdev** directory
    -   Run command **pip install .**
    -   Run **pnp-rma**
3. In Terminal 2
    -   Navigate to rma-ui/dna-app
    -   Run the command **npm install**, once installation is complete
    -   Run the command **npm start**
4. PNP RMA App would be available in [http://localhost:3000](http://localhost:3000)



## Using DNAC-PNP RMA App

1. Open URL [http://localhost:3000](http://localhost:3000) in browser
2. Shows up all the devices avaialable in DNAC PNP UI
![rma-ui-listview.jpg](https://github.com/CiscoDevNet/DNAC-PNP-RMA-App/raw/ReadmeImageURL/images/rma-ui-listview.jpg)
3. Click **Replace** against the device to be replaced
4. Input the new device serial number
![rma-ui-listview.jpg](https://github.com/CiscoDevNet/DNAC-PNP-RMA-App/raw/ReadmeImageURL/images/rma-ui-replace.jpg)
5. The status starts showing up in status column
![rma-ui-device-replace.jpg](https://github.com/CiscoDevNet/DNAC-PNP-RMA-App/raw/ReadmeImageURL/images/rma-ui-device-replace.jpg)
6. Once config fetch stage is complete the app waits for the new device to be contacted in PNP, now remove the old device from the network and hook the new device
7. The new device would call home to the PNP server.
8. Once the new device is connected, the app moves to the next stage, Provisioning where the app accepts the EULA on the new device and replaces the config from the old device on to the new device.


