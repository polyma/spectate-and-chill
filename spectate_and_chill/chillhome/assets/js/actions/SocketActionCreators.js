const StreamConstants = require('../constants/StreamConstants');
const ServerConstants = require('../constants/ServerConstants');
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

export function newSocketMessage(msg) {
  return {
    type: ServerConstants.ActionTypes.SOCKET_MESSAGE,
    payload: msg,
  }
}

export function receiveEvents(events) {
  console.log('RECEIVE EVENTs');
  return {
    type: StreamConstants.ActionTypes.ONLINE_UPDATES,
    payload: events,
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

export function requestRecommendations() {
  return {
    type: StreamConstants.ActionTypes.REQUEST_RECOMMENDATIONS,
  }
}

export function error(string) {
  return {
    type: 'ERROR',
    payload: string,
  }
}

export function setTopStream(twitchName) {
  return {
    type: StreamConstants.ActionTypes.TOP_STREAM,
    payload: twitchName,
  }
}

export function getRecommendations(userId, region) {
  console.log('beginning recommendations request...');
  return function (dispatch) {
    dispatch(requestRecommendations());
    return fetch(window.serverUrl + '/recommendations?summonerName=' + userId + '&region=' + region)
      .then(response => response.json())
      .then(json => {
        // We can dispatch many times!
        // Here, we update the app state with the results of the API call.
        console.log('received result for recommendations', json);
        dispatch(receiveStreams(json));
        dispatch({type: 'UNSET_LOADING', payload: false})
      })
      // .catch(err => dispatch(error(err)));
//NOTE: WE MAY NEED import 'babel-polyfill' http://redux.js.org/docs/advanced/AsyncActions.html
      // In a real world app, you also want to
      // catch any error in the network call.
  }
}
export function getChampionName(championId) {
  console.log('beginning champion ID request...');
  return function (dispatch) {
    return fetch('http://pentasteal.lol/common/champions/na')
      .then(response => response.json())
      .then(json => {
        // We can dispatch many times!
        // Here, we update the app state with the results of the API call.
        dispatch(receiveChampion(json.champion[championId]));
        return json;
      });
}
}

export function receiveChampion(championObj){
  return {
    type: 'CHAMPION',
    payload: championObj,
  }
}
