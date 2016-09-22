import { createStore, applyMiddleware } from 'redux';
var Immutable = require('immutable');

import thunkMiddleware from 'redux-thunk'
import {socketMiddleware} from './middleware/socketMiddleware';

import StreamConstants from './constants/StreamConstants';

var StreamRecord = new Immutable.Record({
  id: 0,
  "displayName":"ERROR",
  "name":"muchisgosu",
  "language":"en",
  "logo":"https://static-cdn.jtvnw.net/jtv_user_pictures/mushisgosu-profile_image-b1c8bb5fd700025e-300x300.png",
  "status":"TSM Gosu - Solo Q - Shadowverse later",
  "currentViews":7333,
  "totalViews":78560127,
  "followers":1096293,
  "spectateURL":"<complete gibberish>",
  "twitchURL":"https://www.twitch.tv/mushisgosu",
  "previewURL_small":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-80x45.jpg",
  "previewURL_medium":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-320x180.jpg",
  "previewURL_large":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-640x360.jpg",
  "championId":67,
  "lane":"",
});

var OnlineRecord = new Immutable.Record({
  id: 0,
  matchId: 0,
});

/*
  Create Reducers
*/
function rootApp(state = Immutable.Map(), action) {
  var stateUpdate =  Immutable.fromJS({
    userId: 0,
    userProfileIcon: 0,
    onlineList: onlineListReducers(state.get('onlineList'), action),
    streams: streamReducers(state.get('streams'), action),
  });
  console.log('rootapp', stateUpdate.toJS());
  return stateUpdate;
}

/*
  Helper functions for initial state
*/
var store = createStore(rootApp, Immutable.Map({
  userId: null,
  userProfileIcon: null,
  onlineList: Immutable.List(),
  streams: Immutable.Map(),
}), applyMiddleware(socketMiddleware,thunkMiddleware));


export function onlineListReducers(state=Immutable.List(), action) {
  switch(action.type) {
    case StreamConstants.ActionTypes.ONLINE_UPDATES:
    //RESET:
    state = Immutable.List(action.payload.id, new OnlineRecord(action.payload));
    return state;
    break;
    default:
    return state;
    console.log('defaulted on online list reducers')
  }
}

export function streamReducers(state=Immutable.Map(), action) {
  switch(action.type) {
    case StreamConstants.ActionTypes.RAW_UPDATES:
      state = state.set(action.payload.id, new StreamRecord(action.payload));
      return state;
    break;
    default:
      return state;
      console.log('defaulted on stream reducers')
  }

}

module.exports = store;
