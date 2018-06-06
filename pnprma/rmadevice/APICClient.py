import os
import time
import logging
from flask import Flask
import logging
from pnprma.rmadevice.dnac_helper import DNACHelper
DEVICE_CONFIG_DIR = 'pnprma/conf/device_conf/'
IMAGE_DIR = 'pnprma/conf/device_images/'
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
logging.captureWarnings(True)
class APICClient:
    client = None
    rma_device = None
    workflow = None
    project = None
    def __init__(self, apic_server_ip, username, password):
        self.client  = DNACHelper(address=apic_server_ip,user=username, password=password)

    def get_pnp_device(self, serial_number=None, state=None):
        # NorthBound API Call to get PNP Projects
        device_map = {}
        devices = self.client.get_device(serialnumber=serial_number, state=state, limit=10000)
        for device in devices:
            device['deviceInfo']['id'] = device['id']
            device_map[device['deviceInfo']['serialNumber']] = device['deviceInfo']

        return devices, device_map

    def get_pnp_device_id(self, serial_number=''):
        device_map = {}
        devices = self.client.get_device(serialnumber=serial_number)
        return devices[0]['id']


    def poll_for_unclaimed(self, serial_no):
        if self.poll_for_pnp_device_states( serial_no, "UNCLAIMED"):
            app.logger.info("Device " + serial_no + " is UNCLAIMED")
            return True
        else:
            app.logger.info("Device " + serial_no + " failed to get UNCLAIMED")
            return False

    def poll_for_provisioned(self, serial_no):
        if self.poll_for_pnp_device_states(serial_no, "PROVISIONED"):
            app.logger.info("Device " + serial_no + " is PROVISIONED")
            return True
        else:
            app.logger.info("Device " + serial_no + " failed to get PROVISIONED")
            return False

    def poll_for_pnp_device_states(self, serial_no, state):
        loop_count = 150
        for i in range(0, loop_count):
            device, _ = self.get_pnp_device(serial_number=serial_no)
            if len(device) > 0:
                app.logger.info("Try " + str(i) + " to get the network_device " + serial_no + ":" + state +
                      ", current network_device state : " + device[0]['deviceInfo']['state'].upper())
                if device[0]['deviceInfo']['state'].upper() in state:
                    return True
                elif "ERROR" in device[0]['deviceInfo']['state'].upper():
                    return False
            else:
                app.logger.info("Waiting for the device " + serial_no + " to connect")
            time.sleep(30)
        return False

    def get_file_id(self, name_space, file_name):
        files = self.client.get_files(namespace=name_space)
        # files = self.client.file.get_file_namespace_by_name_space(name_space=name_space)['response']
        for file in files:
            if file['name'] == file_name:
                return file['id']
        return None

    def upload_file_to_apic(self, name_space, file_name):
        app.logger.info("Uploading " + name_space + ": file :: " + file_name)
        resource_dir = DEVICE_CONFIG_DIR if name_space == 'config' else IMAGE_DIR
        file_path = os.getcwd() + '/' + resource_dir + file_name
        # app.logger.info(self.client.post_file(namespace=name_space,file=file_path))

        # # file_name = file_path[file_path.rfind('/') + 1:]
        file_id = self.get_file_id(name_space, file_name)
        if file_id is not None:
            self.client.delete_config(file_id)
        response = self.client.post_file(namespace=name_space, file=file_path)
        if response:
            return response['response']['id']
        return None

    def start_pnp_device_provisioning(self, id, serial_number, config_id1=None, config_id2=None):
        app.logger.info("Starting Device Provisioning for device :: " + serial_number)

        create_workdflow = {'name': 'pnp_workflow'+str(time.time()), 'description': 'config_upgrade_workflow',
                            'tasks': [{'taskSeqNo': '0', 'name': 'Accept License Config Upgrade',
                                       'type': 'Config', 'configInfo': {
                                    'fileServiceId': config_id1}},{'taskSeqNo': '1', 'name': 'Reloading device',
                                       'type': 'Reload',"waitTimeToReload": 60},
                                      {'taskSeqNo': '2', 'name': 'Device config upgrade',
                                       'type': 'Config', 'configInfo': {
                                    'fileServiceId': config_id2}}]}

        self.workflow = self.client.post_workflow(workflow=create_workdflow)
        create_project = {'name': 'pnp_project'+str(time.time()),
                          'description': 'Sample_pnp_project', 'workflows': [self.workflow['id']]
                          }

        self.project = self.client.post_project(project=create_project)
        claim = {"projectId": self.project['id'], "workflowId": self.workflow['id'],
                 "deviceClaimList": [{"deviceId": id, "templateConfigList": []}]}
        app.logger.info("Claiming Device")
        self.client.post_device_claim(claim_data=claim)

    def post_workflow(self, workflow):
        return self.client.post_workflow(workflow=workflow)