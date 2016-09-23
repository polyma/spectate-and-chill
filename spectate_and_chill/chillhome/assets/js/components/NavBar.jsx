import React from "react"
import Loader from "react-loaders"

export class NavBar extends React.Component {
    render() {
        return (
            <div className="row stretch">
                <div className="col-xs-12 navbar-nav nav-bar">
                    <button type="submit" className="submit-form home-button">
                        <img className="nav-logo" src="../static/specnchill.png"></img>
                    </button>
                    <div className="update-rec">
                        <Loader className="animated zoomIn update-rec" type="ball-grid-pulse" />
                    </div>
                </div>
            </div>
        );
    }
}
