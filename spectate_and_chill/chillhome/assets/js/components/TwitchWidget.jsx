import React from "react"

export class TwitchWidget extends React.Component {
    render() {
        var channelName = "imaqtpie"
        var video = "http://player.twitch.tv/?channel=" + channelName
        var chat = "http://twitch.tv/?channel=" + channelName + "/chat?popout="
        return (
            <div className="row twitch-widget">
                <div className="col-xs-8 media-container">
                    <iframe className="video-player" frameBorder="0" src={video} frameborder="0" scrolling="no" allowfullscreen="true"></iframe>
                </div>
            </div>
        );
    }
}
