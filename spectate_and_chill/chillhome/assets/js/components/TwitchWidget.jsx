import React from "react"

export class TwitchWidget extends React.Component {
    render() {
        //this.props.currentTwitchUrl
        var channelName = this.props.name;
        var video = "http://player.twitch.tv/?channel=" + channelName
        return (
            <div className="row twitch-widget">
                <div className="col-xs-8 media-container">
                    <iframe className="video-player" frameBorder="0" src={video} scrolling="no" allowfullscreen="true"></iframe>
                </div>
            </div>
        );
    }
}
