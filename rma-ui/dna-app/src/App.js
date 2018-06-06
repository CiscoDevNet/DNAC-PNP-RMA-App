import React, { Component } from 'react'
import { ToastContainer, toast } from 'react-toastify'
import "react-toastify/dist/ReactToastify.css"
import axios from 'axios'
import './App.css'
import * as Utils from './helpers/utils'
import {MainTitle} from './components/MainTitle'
import DeviceTable from './components/DeviceTable'
import ReplaceDeviceForm from './components/ReplaceDeviceForm'
const RMA_WEBSERVER='127.0.0.1:7001'
const DEVICE_API = 'http://'+RMA_WEBSERVER+'/device';
const DEVICE_REPLACE_API = DEVICE_API+'/replace';


class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      devices: [],
      currentSerialNumber:'',
      deviceReplacementInProgress:false,
      showModal:false,
      showNotificationMessage:false
    };
  }

 render() {
   return (
        <div className="App">
          <MainTitle/>

          {this.state.devices.length >0 &&
            <DeviceTable devices={this.state.devices}
              deviceReplacementInProgress={this.state.deviceReplacementInProgress}
              handleReplaceDeviceLinkClick={this.handleReplaceDeviceLinkClick}
          />}

          {this.state.showModal && <ReplaceDeviceForm currentSerialNumber={this.state.currentSerialNumber}
            replaceDevice= {this.replaceDevice}
            handleHideModal={this.handleHideModal}
          />}

          {this.state.showNotificationMessage &&
            <ToastContainer closeOnClick={false} position="bottom-right"/>
          }
        </div>
    );
  }

  async componentDidMount() {
    this.fetchDevices();
    this.interval = setInterval(() => this.fetchDevices(), 20000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  fetchDeviceStatus = async(devices) => {
      try {
        const promises = devices.map((device) => {
          return axios.get(DEVICE_API+'/'+device.serialNumber+'/status');
        });

        const response = await Promise.all(promises);
        for (const res of response) {
          const statusObject = res.data;
          const statusObjectKey = Object.keys(statusObject);
          const serialNumber = statusObjectKey[0];
          const index = devices.findIndex((item) => item.serialNumber === serialNumber);
          if (index >= 0) {
            devices[index]['deviceReplacementStatus'] = statusObject;
            if (Utils.isReplacementDeviceInProgress(statusObject[serialNumber])) {
              //Replace device is NOT allowed since only 1 device can be replaced at a time
              this.setState({deviceReplacementInProgress:true});
            }
          }
        }
        this.setState({devices});

      } catch (e) {
        toast.error('Failed to fetch devices status. ' + e.message);
        this.setState({showNotificationMessage:true});
      }
    }


  fetchDevices = async() => {
    try {
      const response = await axios.get(DEVICE_API);
      try {
        this.fetchDeviceStatus(response.data);
      }catch (e) {
        toast.error('Failed to fetch devices status. ' + e.message);
        this.setState({showNotificationMessage:true});
      }
    } catch (e) {
      toast.error('Failed to fetch devices. ' + e.message);
      this.setState({showNotificationMessage:true});
    }
  }

  handleReplaceDeviceLinkClick = (row) => {
    this.setState({currentSerialNumber:row.serialNumber});
    this.handleShowModal();
  }

  handleShowModal = () => {
    this.setState({showModal:true});
  }

  handleHideModal = () => {
    this.setState({showModal:false});
  }

  replaceDevice = async(inputsFromForm) => {
    toast.info("Device replacement request submitted for " + this.state.currentSerialNumber);
    this.setState({showModal:false,showNotificationMessage:true});
    const device = {
       'old_serial_number': this.state.currentSerialNumber,
       'new_serial_number': inputsFromForm.newSerialNumber,
       "device_username": inputsFromForm.deviceUsername,
       "device_password": inputsFromForm.devicePassword,
       "device_enable_password": inputsFromForm.deviceEnablePassword
     }
     try {
       const response = await axios.post(DEVICE_REPLACE_API,device);
     } catch (e) {
       toast.error('Failed to replace device ' + this.state.currentSerialNumber  +'.  ' + e.message);
       this.setState({showNotificationMessage:true});
     }
  }

}

export default App;
