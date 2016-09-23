import React from "react"

export class TwitchWidget extends React.Component {
    render() {
        var channelName = "imaqtpie"
        var video = "http://player.twitch.tv/?channel=" + channelName
        var chat = "http://twitch.tv/?channel=" + channelName + "/chat"
        return (
            <div className="container">
                <div className="row">
                    <div className="col-xs-12">
                        <div className="video-player">
                            <iframe frameborder="0" src={video} height="100%" width="auto" frameborder="0" scrolling="no" allowfullscreen="true">></iframe>
                        </div>
                        <div className="chat-window">
                            <iframe frameborder="0" scrolling="no" id="chat_embed" src={chat} height="100%" width="auto"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
