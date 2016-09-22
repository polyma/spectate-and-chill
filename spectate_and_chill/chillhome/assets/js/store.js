import { createStore, applyMiddleware } from 'redux';
var Immutable = require('immutable');

import thunkMiddleware from 'redux-thunk'
import {socketMiddleware} from './middleware/socketMiddleware';

import StreamConstants from './constants/StreamConstants';

var StreamRecord = new Immutable.Record({
  "displayName":"ERROR",
  "matchId": 0,
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
/*
  Create Reducers
*/
function rootApp(state = Immutable.Map(), action) {
  var stateUpdate =  Immutable.fromJS({
    userId: 0,
    userProfileIcon: 0,
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
  streams: Immutable.List(),
}), applyMiddleware(socketMiddleware,thunkMiddleware));

export function streamReducers(state=Immutable.List(), action) {
  switch(action.type) {
    case StreamConstants.ActionTypes.RAW_UPDATES:
      //RESET:
      state = state.push(new StreamRecord(
          action.payload
          // {
          // "displayName":action.payload,
          // "name":action.payload,
          // "language":action.payload,
          // "logo":action.payload,
          // "status":action.payload,
          // "currentViews":action.payload,
          // "totalViews":action.payload,
          // "followers":action.payload,
          // "spectateURL":action.payload,
          // "twitchURL":action.payload,
          // "previewURL_small":action.payload,
          // "previewURL_medium":action.payload,
          // "previewURL_large":action.payload,
          // "championId":action.payload,
          // "lane":action.payload.lane,
        // }
      ));
      return state;
    break;
    default:
      return state;
      console.log('defaulted on stream reducers')
  }

}

module.exports = store;
