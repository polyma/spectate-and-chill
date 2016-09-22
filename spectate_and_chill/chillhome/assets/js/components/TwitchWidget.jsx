import React from "react"

export class TwitchWidget extends React.Component {
    render() {
        return (
            var channelName = "imaqtpie"
            var video = "http://player.twitch.tv/?channel=" + channelName
            var chat = video + "/chat"
            <div className="video-player col-xs-9">
                <iframe src={video} height="720" width="1280" frameborder="0" scrolling="no" allowfullscreen="true">></iframe>
            </div>
            <div className="chat-window col-xs-3">
                <iframe frameborder="0" scrolling="no" id="chat_embed" src={chat} height="720" width="86"></iframe>
            </div>
        );
    }
}
