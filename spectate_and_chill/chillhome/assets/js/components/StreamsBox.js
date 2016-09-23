import { connect } from 'react-redux'
import React from 'react';
import StreamCard from './StreamCard';

const StreamsBox = ({ streams, onlineList }) => (
  <ul>
    {onlineList.map((stream, i) => {
      var streamObj = streams.get(stream.get('id'));
      if(streamObj) {
        return (
            <div className="col-xs-4">
                  <StreamCard
                    key={i}
                    online={stream.get('matchId')}
                    {...streamObj.toJS()}
                  />
            </div>
        );
      }
    })
    }
  </ul>
)
const mapStateToProps = (state) => {
  return {
    streams: state.get('streams'),
    onlineList: state.get('onlineList'),
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
  }
}

const StreamsBoxContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(StreamsBox)

export default StreamsBoxContainer
