import json
from pnprma.rmadevice import File

CONF_DIR = 'pnprma/conf/'

class Inputs:
    rmadevice = None

    def __init__(self):
        with open(CONF_DIR + 'inputs.json') as data_file:
            data = json.load(data_file)
            self.eem_enable_config_name = data['eem_enable_config_name']
            self.apic_server_ip = data['apic_server_ip']
            self.username = data['username']
            self.password = data['password']