import { createStore, applyMiddleware } from 'redux';
var Immutable = require('immutable');

import thunkMiddleware from 'redux-thunk'
import {socketMiddleware} from './middleware/socketMiddleware';

import StreamConstants from './constants/StreamConstants';
import ServerConstants from './constants/ServerConstants';

var StreamRecord = new Immutable.Record({
  id: 0,
  "displayName":"ERROR",
  "name":"muchisgosu",
  "language":"en",
  "logo":"https://static-cdn.jtvnw.net/jtv_user_pictures/rush-profile_image-b1c8bb5fd700025e-300x300.png",
  "status":"TSM Gosu - Solo Q - Shadowverse later",
  "currentViews":7333,
  "totalViews":78560127,
  "followers":1096293,
  "spectateURL":"<complete gibberish>",
  "twitchURL":"https://www.twitch.tv/rush",
  "previewURL_small":"https://static-cdn.jtvnw.net/previews-ttv/live_user_rush-80x45.jpg",
  "previewURL_medium":"https://static-cdn.jtvnw.net/previews-ttv/live_user_rush-320x180.jpg",
  "previewURL_large":"https://static-cdn.jtvnw.net/previews-ttv/live_user_rush-640x360.jpg",
  "championId":67,
  "lane":"",
  "score":0
});

var OnlineRecord = new Immutable.Record({
  id: 0,
  matchId: 0,
  twitchLive: 0,
});

/*
  Create Reducers
*/
function rootApp(state = Immutable.Map(), action) {
  var stateUpdate =  Immutable.fromJS({
    userId: 0,
    userProfileIcon: 0,
    onlineList: onlineListReducers(state.get('onlineList'), action, state),
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
}), applyMiddleware(socketMiddleware, thunkMiddleware));


export function onlineListReducers(state=Immutable.List(), action, rootState) {
  console.log('online list reducers!', action);
  switch(action.type) {
    case ServerConstants.ActionTypes.SOCKET_MESSAGE:
      //Checkagainst previous list and get diffs
      //get offlines of previous
      var offline = state.filter(x => (x.matchId === 0))
      //get all onlines of new
      var online = action.payload.filter(y => {
        if(y.matchId !== 0) {
          //online
          return y
        }
      });
      var new_online = offline.filter((off) => {
        var bO = false;
        online.forEach(on => {
          if(on.id === off.get('id')) { //TODO: check types match
            bO = true;
          }
        });
        if(bO === true) {
          return off;
        }
      });
      console.log(offline, online, new_online)
      //Now check if new online is in our system
      if(new_online.count() !== 0) {
        console.log('new online!', new_online.toJS())
        new_online.forEach(function(n) {
          console.log(rootState)
          if(rootState.get('streams').get(n.id)) {
            console.log('woo!');
            window.alert('YES! ' + n.id + ' is online!');
          }
        });
      }
      //TODO: convert to middleware
      //RESET list
      state = Immutable.List(action.payload.map((update) => {
        return new OnlineRecord(update);
      }));
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
      action.payload.forEach(function(stream) {
        state = state.set(stream.id, new StreamRecord(stream));
      })
      console.log('Received updates from recommendation endpoint', state);
      return state;
    break;
    default:
      return state;
      console.log('defaulted on stream reducers')
  }

}

module.exports = store;
