import React from "react"

export class NavBar extends React.Component {
    render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-xs-12 navbar-nav nav-bar">
                        <img className="logo" src="../static/specnchill.png"></img>
                    </div>
                </div>
            </div>
        );
    }
}
