import * as Constants from "./constants";
import * as Validator from './validator'


export const isReplacementDeviceInProgress = (state) => {
  if (state) {
    return (state[Constants.FETCH_CONFIG].progress === Constants.IN_PROGRESS ||
     state[Constants.WAITING_FOR_NEW_DEVICE].progress === Constants.IN_PROGRESS ||
     state[Constants.PROVISION_NEW_DEVICE].progress === Constants.IN_PROGRESS);
  }
  return false;
};

export const getStatusColor = (status) => {
    switch(status) {
      case Constants.NOT_STARTED: return "#D3D3D3";
      case Constants.IN_PROGRESS: return "#03a9f4";
      case Constants.FAILED: return "#ff0000";
      case Constants.COMPLETE: return "#6fba1c";
      default: return "#D3D3D3";
    }
}

export const getCheckMark = (status) => {
  if (status) {
    if (status === Constants.COMPLETE) {
      return "✔ ";
    }
    return "";
  }
}

export const getValidateSerialNumberState = (serialNumber) => {
  if (serialNumber) {
    if (serialNumber.length === 0) {
      return null;
    }

    const validation = Validator.isValidSerialNumber(serialNumber);
    if (validation) {
      return Constants.SUCCESS;
    }

    return Constants.ERROR;
  }
}
