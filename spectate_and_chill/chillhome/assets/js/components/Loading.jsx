import React from "react"
import Loader from "react-loaders"

export class Loading extends React.Component {
    render() {
        let loader = <Loader className="animated zoomIn" type="ball-scale-ripple" />
        return (
            <div>
                <img className="snax-load" src="../static/porosnax.png"></img>
                <div className="load-anim">
                    {loader}
                </div>
            </div>
        );
    }
}
