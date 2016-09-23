import React from "react"
import Loader from "react-loaders"

export class Loading extends React.Component {
    render() {
        let loader = <Loader className="animated zoomIn" type="ball-grid-pulse" />
        return (
            <div className="load-anim">
                {loader}
            </div>
        );
    }
}
