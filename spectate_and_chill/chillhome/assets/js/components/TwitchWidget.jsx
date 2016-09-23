import React from "react"

import {connect} from 'react-redux';

export class Twitch extends React.Component {
    render() {
        //this.props.currentTwitchUrl
        var channelName = this.props.name;
        var video = "http://player.twitch.tv/?channel=" + channelName
        return (
            <div className="row twitch-widget">
                <div className="col-xs-8 col-xs-offset-2 media-container">
                    <iframe className="video-player" frameBorder="0" src={video} scrolling="no" allowfullscreen="true"></iframe>
                </div>
            </div>
        );
    }
}
const mapStateToProps = (state) => {
  return {
    name: state.get('topStream'),
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
  }
}
const TwitchWidget = connect(
  mapStateToProps,
  mapDispatchToProps
)(Twitch)

export default TwitchWidget
