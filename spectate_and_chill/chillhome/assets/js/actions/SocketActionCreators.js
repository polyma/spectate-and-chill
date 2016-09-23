const ServerConstants = require('../constants/ServerConstants');
const StreamConstants = require('../constants/StreamConstants');
import fetch from 'isomorphic-fetch'


export function newSocket(socket) {
  return {
    type: ServerConstants.ActionTypes.NEW_SOCKET_CONNECTION,
    socket: socket,
  }
}

export function joinStream(id) {
  return {
    type: ServerConstants.ActionTypes.JOIN_STREAM,
    streamId: id,
  }
}

export function receiveStreams(streams) {
  return {
    type: StreamConstants.ActionTypes.RAW_UPDATES,
    payload: streams,
  }
}

export function disconnect() {
  return {
    type: ServerConstants.ActionTypes.DISCONNECT_SERVER,
  }
}

export function getRecommendations() {
  return {
    type: StreamConstants.ActionTypes.REQUEST_RECOMMENDATIONS,
  }
}

export function getRecommendations(userId) {
  return function (dispatch) {
    dispatch(getRecommendations());
    return fetch(window.serverUrl + '/recommendations?user_id=' + userId)
      .then(response => response.json())
      .then(json => {
        // We can dispatch many times!
        // Here, we update the app state with the results of the API call.
        console.log('received result for recommendations', json);
        dispatch(receiveStreams(json));
      })
//NOTE: WE MAY NEED import 'babel-polyfill' http://redux.js.org/docs/advanced/AsyncActions.html
      // In a real world app, you also want to
      // catch any error in the network call.
  }
}
