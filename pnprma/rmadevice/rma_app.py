from .Inputs import Inputs
from .ScanDevices import ScanDevices
from .APICClient import APICClient
from .Poller import Poller
from .States import States

class RMAApp:
    status = None
    def __int__(self):
        status="Not_Started"

    def scan_devices(self, device_ip, serial_number, device_username, device_password, device_enable_password):
        status = "Fetching_Config"
        devices = {}
        inputs = Inputs()
        scan = ScanDevices(device_ip, serial_number, device_username, device_password, device_enable_password)
        if not scan.start():
            return False
        else:
            return True
        status = "Config_Fetch_Complete"



    def rma_device(self,old_serial_number, new_serial_number):
        inputs = Inputs()
        client = APICClient(inputs.apic_server_ip, inputs.username, inputs.password)
        eem_config_file_id = client.upload_file_to_apic(name_space='config',
                                                        file_name=inputs.eem_enable_config_name)
        poll = Poller(client, eem_config_file_id, old_serial_number, new_serial_number)
        poll.start()


    def start_rma(self,old_serial_no, new_serial_number, device_ip, device_username, device_password, device_enable_password):
        state = States()
        state.putState(old_serial_no, state="FETCH_CONFIG", progress="IN_PROGRESS")
        if self.scan_devices(device_ip, old_serial_no, device_username, device_password, device_enable_password):
            state.putState(old_serial_no, state="FETCH_CONFIG", progress="COMPLETE")
            self.rma_device(old_serial_no, new_serial_number)
