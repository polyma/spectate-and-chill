import React from "react"

export class NavBar extends React.Component {
    render() {
        return (
            <div className="row stretch">
                <div className="col-xs-12 navbar-nav nav-bar">
                    <img className="nav-logo" src="../static/specnchill.png"></img>
                </div>
            </div>
        );
    }
}
