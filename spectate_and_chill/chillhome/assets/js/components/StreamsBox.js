import { connect } from 'react-redux'
import React from 'react';
import StreamCard from './StreamCard';
import { setTopStream } from '../actions/SocketActionCreators';
const StreamsBox = ({ streams, onlineList, setTopOnline }) => (
  <div className="row">
    {console.log('loading streams box', streams)}
    {rankStreams(streams, onlineList, setTopOnline)}
  </div>
)
const mapStateToProps = (state) => {
  return {
    streams: state.get('streams'),
    onlineList: state.get('onlineList'),
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
    setTopOnline: function(twitchName) {
      dispatch(setTopStream(twitchName));
    }
  }
}

var rankStreams = function rankStream(streams, onlineList, setTopOnline) {
  if(streams.size !== 0) {
    var s = streams.toIndexedSeq().toArray().map((stream, i) => {
      var isOnline = false;
      onlineList.map((online) => {
        if(stream.get('id') === online.id && online.matchId !== 0) {
          isOnline = true;
        }
      });
      return {
        isOnline,
        name: stream.get('name'),
        stream,
        score: stream.get('score'),
      }
    });
    s.sort(function(obj1, obj2) {
      return obj1.score - obj2.score;
    });
    //now order
    var onlines = s.map(function(m, x) {
      if(m.isOnline) {
        return (
          <div key={x + "o"} top={m.name} className="col-xs-4">
            <StreamCard

              score={m.score}
              online={m.isOnline}
              {...m.stream.toJS()}
            />
          </div>
        );
      }
    });
    var offlines = s.map(function(m, x) {
      if(!m.isOnline) {
        return (
          <div key={x + "f"} className="col-xs-4">
            <StreamCard

              score={m.score}
              online={m.isOnline}
              {...m.stream.toJS()}
            />
          </div>
        );
      }
    });
    var full_list = onlines.concat(offlines)
    setTopOnline(full_list[0]);
    return full_list;
  }
  else {
    return null;
  }
}

const StreamsBoxContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(StreamsBox)

export default StreamsBoxContainer
