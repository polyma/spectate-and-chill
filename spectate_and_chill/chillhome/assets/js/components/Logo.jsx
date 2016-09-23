import React from "react"

export class Logo extends React.Component {
    render() {
        return (
            <div className="row">
                <div className="col-xs-12 logo-container">
                    <div className="logo">
                        <img src="../static/specnchill.png"></img>
                    </div>
                </div>
            </div>
        );
    }
}
