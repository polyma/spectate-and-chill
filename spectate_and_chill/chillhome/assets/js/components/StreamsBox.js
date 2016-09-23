import { connect } from 'react-redux'
import React from 'react';
import StreamCard from './StreamCard';

const StreamsBox = ({ streams, onlineList }) => (
  <div className="row">
    {console.log('loading streams box', streams)}
    {streams.size !== 0 ? streams.toIndexedSeq().toArray().map((stream, i) => {
      var isOnline = false;
      onlineList.map((online) => {
        if(stream.get('id') === online.id && online.matchId !== 0) {
          isOnline = true;
        }
      });
      return (
        <div className="col-xs-4">
          <StreamCard
            key={i}
            online={isOnline}
            {...stream.toJS()}
          />
        </div>
      );
    })
    : null}
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
  }
}

const StreamsBoxContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(StreamsBox)

export default StreamsBoxContainer
