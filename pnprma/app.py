from flask import Flask
from pnprma.rmadevice.APICClient import APICClient
from pnprma.rmadevice.Inputs import Inputs
import json
from flask import request
from flask_cors import CORS
from pnprma.rmadevice.States import States
from pnprma.rmadevice.rma_app import RMAApp
from flask import jsonify
import logging


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

CORS(app)

@app.route("/")
def hello():
    app.logger.info("/hello")
    app.logger.setLevel(logging.INFO)
    return "Hello World!"


def get_non_errorred_devices(client):
    _, apic_devices = client.get_pnp_device()
    non_provisioned_devices = [apic_devices[dev] for dev in apic_devices if apic_devices[dev]['state'] not in ['Error']]
    return non_provisioned_devices

@app.route("/device")
def get_devices():
    inputs = Inputs()
    client = APICClient(inputs.apic_server_ip, inputs.username, inputs.password)
    apic_devices = get_non_errorred_devices(client)
    # output = [device for device in apic_devices]
    # app.logger.info(output)
    return json.dumps(apic_devices)


@app.route("/device/<serial_no>/status")
def get_status(serial_no):
    state = States()
    return jsonify({serial_no: state.getState(serial_no)})
    # return jsonify({"serial_number": serial_no, "state": jsonify(state.getState(serial_no))})


@app.route("/device/replace", methods=["POST"])
def replace():
    if 'old_serial_number' in request.json and 'new_serial_number' in request.json and \
            'device_username' in request.json and 'device_password' in request.json and  \
            'device_enable_password' in request.json:
        old_serial_number = request.json['old_serial_number']
        new_serial_number = request.json['new_serial_number']
        device_username = request.json['device_username']
        device_password = request.json['device_password']
        device_enable_password = request.json['device_enable_password']
        inputs = Inputs()
        client = APICClient(inputs.apic_server_ip, inputs.username, inputs.password)
        dev,_=client.get_pnp_device(serial_number=old_serial_number)
        try:
            device_ip = dev[0]['deviceInfo']['httpHeaders'][0]['value']
        except:
            error_msg="Device is not available in pnp app"
            app.logger.info(error_msg)
            states = States()
            states.putState(old_serial_number, "FETCH_CONFIG", "FAILED", error_msg)
            return error_msg

        rma = RMAApp()
        rma.start_rma(old_serial_number, new_serial_number, device_ip, device_username, device_password, device_enable_password)
        return request.json['old_serial_number'] + ":" + request.json['new_serial_number']
    else:
        return "Send request with body example {'old_serial_number': '12345678', 'new_serial_number': 'ABCDEFGH'}"
    return str(request.json)

def main():
    app.run(host='0.0.0.0', port=7001, threaded=True)
    # app.run(port=7001, threaded=True)


if __name__ == '__main__':
    main()
