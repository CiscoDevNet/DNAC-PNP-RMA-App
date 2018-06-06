import React, { Component } from 'react'
import PropTypes from 'prop-types';
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table'
import { Button, Panel} from 'react-bootstrap'
import {Timeline, TimelineEvent} from 'react-event-timeline'
import "react-toastify/dist/ReactToastify.css"
import ReactJson from 'react-json-view'
import '../App.css'
import * as Utils from '../helpers/utils'
import * as Constants from '../helpers/constants'

class DeviceTable extends Component {

  // It's a data format example.
  replaceDeviceStatusColumnFormatter = (cell, row, formatExtraData, rowIdx) => {
    const deviceSerialnumber =  row.serialNumber;
    if (!row.deviceReplacementStatus) return;
    const status = row.deviceReplacementStatus[deviceSerialnumber];
    if (status) {
      if (status[Constants.FETCH_CONFIG].progress === Constants.NOT_STARTED) {
        return (<p>None</p>);
      }
      /*
      status:
      NOT_STARTED
      IN_PROGRESS "#6fba1c"
      FAILED
      COMPLETE "#03a9f4"
      */
      return (
        <Panel id="device-replacement" defaultExpanded>
          <Panel.Heading>
            <Panel.Toggle componentClass="a">Show/Hide status</Panel.Toggle>
          </Panel.Heading>
          <Panel.Collapse>
            <Panel.Body>
              <div><Timeline>
                   <TimelineEvent
                     title={Constants.FETCH_CONFIG}
                     titleStyle={{fontWeight: "bold"}}
                     createdAt={status[Constants.FETCH_CONFIG].timestamp}
                     subtitle={Utils.getCheckMark(status[Constants.FETCH_CONFIG].progress) + status[Constants.FETCH_CONFIG].progress}
                     subtitleStyle={{color: Utils.getStatusColor(status[Constants.FETCH_CONFIG].progress)}}
                     icon={<i />}
                     iconColor={Utils.getStatusColor(status[Constants.FETCH_CONFIG].progress)}
                   >
                   <p>Fetch config from device {deviceSerialnumber}.</p>
                   <p>{status[Constants.FETCH_CONFIG].msg}</p>
                   </TimelineEvent>
                   <TimelineEvent
                     title={Constants.WAITING_FOR_NEW_DEVICE}
                     createdAt={status[Constants.WAITING_FOR_NEW_DEVICE].timestamp}
                     subtitle={Utils.getCheckMark(status[Constants.WAITING_FOR_NEW_DEVICE].progress)  + status[Constants.WAITING_FOR_NEW_DEVICE].progress}
                     subtitleStyle={{color: Utils.getStatusColor(status[Constants.WAITING_FOR_NEW_DEVICE].progress)}}
                     icon={<i />}
                     iconColor={Utils.getStatusColor(status[Constants.WAITING_FOR_NEW_DEVICE].progress)}
                   >
                   <p>Wait for new device to replace device {deviceSerialnumber}</p>
                   <p>{status[Constants.WAITING_FOR_NEW_DEVICE].msg}</p>
                   </TimelineEvent>
                   <TimelineEvent
                     title={Constants.PROVISION_NEW_DEVICE}
                     titleStyle={{fontWeight: "bold"}}
                     createdAt={status[Constants.PROVISION_NEW_DEVICE].timestamp}
                     subtitle={Utils.getCheckMark(status[Constants.PROVISION_NEW_DEVICE].progress) + status[Constants.PROVISION_NEW_DEVICE].progress}
                     subtitleStyle={{color: Utils.getStatusColor(status[Constants.PROVISION_NEW_DEVICE].progress)}}
                     icon={<i />}
                     iconColor={Utils.getStatusColor(status[Constants.PROVISION_NEW_DEVICE].progress)}
                   >
                   Provision new device.  {status[Constants.PROVISION_NEW_DEVICE].msg}
                   </TimelineEvent>
                 </Timeline></div>
            </Panel.Body>
          </Panel.Collapse>
      </Panel>
      );
    } else {
      return (<p>None</p>);
    }
  }

  ipAddressFormatter = (cell, row, formatExtraData, rowIdx) => {
    if (row.httpHeaders && Array.isArray(row.httpHeaders)) {
      return (<p>{row.httpHeaders[0].value}</p>);
    }
    return '';
  }

  replaceDeviceColumnFormatter = (cell, row, formatExtraData, rowIdx) => {
    /*replace device one at a time*/
    return (
      <Button bsStyle="link" disabled={this.props.deviceReplacementInProgress}
        onClick={() => {this.props.handleReplaceDeviceLinkClick(row)}}>Replace</Button>
      );
  }

  isExpandableRow = (row) => {
    if (row.serialNumber) return true;
    else return false;
  }

  expandComponent = (row) => {
    return (
      <div className="details"><ReactJson src={row} /></div>
    );
  }

  render() {
    return <div className="table"><BootstrapTable
     data={ this.props.devices }
     expandableRow={this.isExpandableRow}
     expandComponent={this.expandComponent}
     expandColumnOptions={{expandColumnVisible: true}}
     options={{expandRowBgColor: 'rgb(190,190,190)',expandBy: 'column'}}
     search={true}>
         <TableHeaderColumn dataField='serialNumber' isKey={true} width='150px'>Serial Number</TableHeaderColumn>
         <TableHeaderColumn dataField='pid' expandable={ false } width='150px'>Product ID</TableHeaderColumn>
         <TableHeaderColumn dataField='hostname' expandable={ false } width='150px'>Hostname</TableHeaderColumn>
         <TableHeaderColumn dataField='ip' expandable={ false } dataFormat={this.ipAddressFormatter} width='150px'>IP Address</TableHeaderColumn>
         <TableHeaderColumn dataField='' expandable={ false }
               dataFormat={this.replaceDeviceStatusColumnFormatter}>Replacement Status</TableHeaderColumn>
             <TableHeaderColumn dataField='button' expandable={ false }
           dataFormat={this.replaceDeviceColumnFormatter}  width='100px'>Action</TableHeaderColumn>
     </BootstrapTable></div>
  }
}

DeviceTable.propTypes = {
  devices: PropTypes.array.isRequired,
  handleReplaceDeviceLinkClick: PropTypes.func.isRequired,
  deviceReplacementInProgress: PropTypes.bool
}

DeviceTable.default = {
  deviceReplacementInProgress: false
}

export default DeviceTable;
