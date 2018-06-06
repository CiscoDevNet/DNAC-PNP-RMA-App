import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { Button, Form, Col, FormGroup,
  ControlLabel, FormControl, Modal} from 'react-bootstrap'
import * as Utils from '../helpers/utils'
import * as Constants from '../helpers/constants'

class ReplaceDeviceForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      deviceUsername:'',
      devicePassword:'',
      deviceEnablePassword:'',
      newSerialNumber:'',
      showModalLInda:true
    };
  }

  handleChange = (e) => {
    e.preventDefault();

    switch (e.target.id) {
      case 'newSerialNumberText': this.setState({ newSerialNumber: e.target.value });
      break;
      case 'deviceUsername': this.setState({ deviceUsername: e.target.value });
      break;
      case 'devicePassword': this.setState({ devicePassword: e.target.value });
      break;
      case 'deviceEnablePassword': this.setState({ deviceEnablePassword: e.target.value });
      break;
      default:console.log("invalid input " + e.target.id);
    }
  }

  handleReplaceDeviceButtonClick = () => {
    this.props.replaceDevice(this.state);
  }

  render() {

    const areAllFieldsFilled = (this.state.newSerialNumber.length>0 &&
      this.state.deviceUsername.length>0 &&
      this.state.devicePassword.length>0 &&
      this.state.deviceEnablePassword.length>0 &&
      Utils.getValidateSerialNumberState(this.state.newSerialNumber) === Constants.SUCCESS);

      return (
        <div><Modal
            show={true}
            onHide={this.props.handleHideModal}
            container={this}
            aria-labelledby="contained-modal-title">
           <Modal.Header closeButton>
              <Modal.Title id="contained-modal-title">
                <h3>Replace device <font color="red">{this.props.currentSerialNumber}</font></h3>
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="txt-label">Please provide credentials of old device {this.props.currentSerialNumber}</div>
                <Form horizontal id='myForm'
                  className="form"
                  onSubmit={ this.props.replaceDevice.bind( this )}
                  ref={ form => this.replaceForm = form }>
                     <FormGroup controlId="deviceUsername">
                      <Col componentClass={ControlLabel} sm={3} bsSize="small" >
                        Username
                      </Col>
                      <Col sm={8}>
                          <FormControl bsSize="small"
                            type="text"
                            placeholder="User name"
                            value={this.state.deviceUsername}
                            onChange={this.handleChange}/>
                          <FormControl.Feedback />
                      </Col>
                    </FormGroup>

                    <FormGroup controlId="devicePassword" ref="devicePassword">
                       <Col componentClass={ControlLabel} sm={3}>
                         Password
                       </Col>
                       <Col sm={8}>
                           <FormControl bsSize="small"
                             type="password"
                             placeholder="Password"
                             value={this.state.devicePassword}
                             onChange={this.handleChange}/>
                           <FormControl.Feedback />
                       </Col>
                    </FormGroup>

                    <FormGroup controlId="deviceEnablePassword">
                      <Col componentClass={ControlLabel} sm={3}>
                        Enable Password
                      </Col>
                      <Col sm={8}>
                          <FormControl bsSize="small"
                            type="password"
                            placeholder="Enable Password"
                            value={this.state.deviceEnablePassword}
                            onChange={this.handleChange}/>
                          <FormControl.Feedback />
                      </Col>
                    </FormGroup>
                    <div className="txt-label-morespace">New Serial Number</div>

                    <FormGroup controlId="newSerialNumberText"
                        validationState={Utils.getValidateSerialNumberState(this.state.newSerialNumber)}>
                        <Col componentClass={ControlLabel} sm={3}>
                          Serial number
                        </Col>
                        <Col sm={8}>
                            <FormControl
                              type="text" bsSize="small"
                              placeholder="New serial number"
                              value={this.state.newSerialNumber}
                              onChange={this.handleChange}/>
                            <FormControl.Feedback />
                        </Col>
                      </FormGroup>
                    </Form>
            </Modal.Body>
            <Modal.Footer>
              <Button bsStyle="primary" disabled={!areAllFieldsFilled}
                onClick={this.handleReplaceDeviceButtonClick}>OK to replace</Button>
            </Modal.Footer>
          </Modal></div>
      );
  }
}

ReplaceDeviceForm.propTypes = {
  currentSerialNumber: PropTypes.string.isRequired,
  replaceDevice: PropTypes.func.isRequired,
  handleHideModal: PropTypes.func.isRequired
}

export default ReplaceDeviceForm;
