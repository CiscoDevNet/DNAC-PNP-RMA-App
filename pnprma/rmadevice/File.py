import csv
import os

CONF_DIR = 'pnprma/conf/'

class CSVRow:
    username = None
    password = None
    enable_password = None
    old_serial_number = None
    rma_serial_number = None
    image_name = None
    status = None
    rmaed_on = None

    def __init__(self, username, password, enable_password, rma_serial_number=None,
                 old_serial_number=None, image_name = None, status=None):
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.old_serial_number = old_serial_number
        self.rma_serial_number = rma_serial_number
        self.status = status
        self.image_name = image_name

    def set_old_serial_number(self, old_serial_number):
        self.old_serial_number = old_serial_number

    def set_status(self, status):
        self.status = status

    def set_image_name(self, image_name):
        self.image_name = image_name

    def set_rmaed_on(self, date):
        self.rmaed_on = date


def write_to_csv(csv_file_name, rows):
    with open(CONF_DIR + csv_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        first_row = ['username', 'password', 'enable_password',
                     'rma_serial_number',
                     'old_serial_number', 'image_name', 'status', 'rmaed_on']
        writer.writerow(first_row)
        for row in rows:
            device = [row.device_ip, row.username, row.password, row.enable_password]
            if row.rma_serial_number:
                device.append(row.rma_serial_number)
            if row.old_serial_number:
                device.append(row.old_serial_number)
            if row.image_name:
                device.append(row.image_name)
            if row.status:
                device.append(row.status)
            if row.rmaed_on:
                device.append(row.rmaed_on)
            writer.writerow(tuple(device))
        csvfile.close()

def read_csv(csv_file_name):
    csv_rows = []
    rows = None
    with open(CONF_DIR + csv_file_name, 'r') as csvfile:
        rows = list(csv.reader(csvfile))[1:]
        csvfile.close()
    for row in rows:
        csv_row = None
        if len(row) >= 3:
            csv_row = CSVRow(row[0], row[1], row[2])
            return csv_row


def write_old_serial_number_to_csv(csv_file_name, csv_devices, devices):
    with open('new_' + csv_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        first_row = ['username', 'password', 'enable_password', 'rma_serial_number',
                     'old_serial_number','status','rmaed_on']
        writer.writerow(first_row)
        for device in devices:
            if device in csv_devices:
                devices[device].append(csv_devices[device])
                writer.writerow((devices[device]))
        csvfile.close()


def remove_csv(csv_file_name):
    os.remove(CONF_DIR + csv_file_name)


def rename_csv(new_name, old_name):
    os.rename(CONF_DIR + new_name, CONF_DIR + old_name)