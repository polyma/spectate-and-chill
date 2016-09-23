import React from "react"
import Loader from "react-loaders"

export class Loading extends React.Component {
    render() {
        let loader = <Loader className="animated zoomIn" type="ball-scale-ripple" />
        return (
            <div>
              <div className="load-anim">
                {loader}
                Loading... {this.props.status}
                </div>
            </div>
        );
    }
}
