import React from 'react'
import { Jumbotron } from 'react-bootstrap'
export const MainTitle = () => {
  const style = {
    textAlign: "center",
    color: "#328CC1",
    fontSize: "medium"
  }

  return <div><Jumbotron>
        <h1>Auto Device Replacement</h1>
        <div style={style}> Automatic replacement of earlier PNP Provisioned non-working device,
            with new device of same platform/SKU type.</div>
            <div style={style}>Bring new device to provisioned state
            by restoring configuration from old device.</div>
          <p1>Powered by DevNet Cisco DNA APIs</p1>
    </Jumbotron></div>;
}
