import paramiko
import time
import re
from flask import Flask
from pnprma.rmadevice.States import States
import logging


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
DEVICE_CONFIG = 'pnprma/conf/device_conf/'
POST_EEM_ENABLE = 'EEM-Enable-RSA.txt'

class ScanDevices():
    ip_address = None
    username = None
    password = None
    enable_password = None
    device_data = {}

    def __init__(self, ip_address, serial_number, username, password, enable_password):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.serial_number = serial_number
        self.enable_password = enable_password

    def start(self):
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.load_system_host_keys()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        app.logger.info("Fetching config from device " + self.ip_address + " : " + self.username + " : " + self.password)
        try:
            remote_conn_pre.connect(hostname=self.ip_address, username=self.username,
                                    password=self.password, look_for_keys=False, allow_agent=False)
        except:
            app.logger.info("Device not able to SSH")
            states = States()
            states.putState(self.serial_number, "FETCH_CONFIG", "FAILED", "Device not able to SSH")
            return False
        remote_conn = remote_conn_pre.invoke_shell()
        remote_conn.send('terminal length 0\r\n')
        remote_conn.send('enable \r')
        time.sleep(3)
        response = remote_conn.recv(9999)
        if b'Password' in response:
            remote_conn.send(self.enable_password + '\n')
            time.sleep(2)

        remote_conn.send('sh inventory | inc PID\n')
        time.sleep(2)
        serial_number_response = remote_conn.recv(65535)
        # regexp_serial_no = r'.*SN: +(\S+)'
        regexp_serial_no = r'.*SN:\s(\S+)'
        serial_no_line = ""
        for line in serial_number_response.splitlines():
            line = line.decode('utf-8')
            if "SN:" in line:
                serial_no_line = line
                break;
        match_serial_no = re.match(regexp_serial_no, serial_no_line)
        if match_serial_no:
            serial_no = match_serial_no.group(1)

        remote_conn.send('sh run\n')
        time.sleep(6)
        sh_run_response = remote_conn.recv(65535)

        if serial_no:
            with open(DEVICE_CONFIG + serial_no, 'w') as device_config_file:
                sh_run_response_sting = sh_run_response.decode('utf-8')
                start_index = sh_run_response_sting.find('!')
                end_index = sh_run_response_sting.rfind('end')
                config = sh_run_response_sting[start_index:end_index]
                config = re.sub('license udi .*\n','', config)
                config = re.sub('platform qfp utilization monitor load 80','',config)
                config = re.sub('transport input none', '', config)
                eem_script = open(DEVICE_CONFIG + POST_EEM_ENABLE, 'r')
                config = config + eem_script.read() +'end\n'
                # config = config +'end\n'
                device_config_file.write(config)
            self.device_data[self.ip_address] = {}
            self.device_data[self.ip_address]['old_serial_no'] = serial_no
        return True

