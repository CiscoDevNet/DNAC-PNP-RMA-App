import time
from .States import States
from flask import Flask
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

class Poller():
    client = None
    new_serial_number = None
    eem_config_id = None
    old_serial_number = None
    image_name = None
    status = None
    rmaed_on = None
    device_id = None

    def __init__(self, client, eem_config_file_id, old_serial_number, new_serial_number):
        self.client = client
        self.eem_config_id = eem_config_file_id
        self.new_serial_number = new_serial_number
        self.old_serial_number = old_serial_number

    def config_and_provision_device(self, serial_number, config_id1, config_id2):
        state = States()
        state.putState(self.old_serial_number, state="WAITING_FOR_NEW_DEVICE", progress="IN_PROGRESS")
        if not self.client.poll_for_unclaimed(serial_no=serial_number):
            app.logger.info("New RMA Device has not yet contacted!")
            states = States()
            states.putState(self.old_serial_number, "WAITING_FOR_NEW_DEVICE", "FAILED", "New RMA Device has not yet contacted!")
            return False
        state.putState(self.old_serial_number, state="WAITING_FOR_NEW_DEVICE", progress="COMPLETE")
        self.device_id = self.client.get_pnp_device_id(serial_number=serial_number)
        self.client.start_pnp_device_provisioning(id=self.device_id, serial_number=serial_number,
                                                  config_id1=config_id1, config_id2=config_id2)
        state.putState(self.old_serial_number, state="PROVISION_NEW_DEVICE", progress="IN_PROGRESS")
        if self.client.poll_for_provisioned(serial_no=serial_number):
            state.putState(self.old_serial_number, state="PROVISION_NEW_DEVICE", progress="COMPLETE")
            return True
        else:
            state.putState(self.old_serial_number, state="PROVISION_NEW_DEVICE", progress="FAILED", msg="Provisioning has failed")
            return False

    def start(self):
        device_config_file_id = self.client.upload_file_to_apic(name_space='config',
                                                                file_name=self.old_serial_number)


        app.logger.info("Old Device : " + self.old_serial_number + " to be RMAed with " + self.new_serial_number)

        # Claim the network_device for the first time
        assert self.config_and_provision_device(serial_number=self.new_serial_number,
                                                config_id1=self.eem_config_id,
                                                config_id2=device_config_file_id), "Failed Config Provision"

        self.status = "RMA_SUCCESSFULL"
        self.rmaed_on = time.strftime("%Y-%m-%d %H:%M")