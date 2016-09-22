import React from "react"
import {Twitchwidget} from "TwitchWidget"

export class StreamView extends React.Component {
    render() {
        return (
            <div className="row">
                <TwitchWidget />
            </div>
        );
    }
}
