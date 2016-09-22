var Constants = require('../constants/ServerConstants');
var socket = null;

/*
  SET UP SOCKET CONNECTION
*/
var io = require('socket.io-client');
socket = io.connect('ws://localhost:8080'); //NOTE: need to send user id for this to work
socket.on('connect', function() {
  console.log('connected to server!');
});

/*
  REDUX MIDDLEWARE
*/
export function socketMiddleware(store) {
  return next => action => {
    const result = next(action);
    // if(action.type ===  Constants.ActionTypes.NEW_SOCKET_CONNECTION) {
    //   console.log('Registered new socket connection with middleware');
    //   setSocket(action.socket);
    //   return result;
    // }
    if (socket) {
      backendSwitch(action);
    }

    return result;
  };
}

/*
  Switch for events from the backend
*/
import {receiveStreams, disconnect} from '../actions/SocketActionCreators';
var reduxStore = require('../store');
export function backendSwitch(msg) {
  switch(msg.event) {
    case 'streams':
      reduxStore.dispatch(receiveStreams(msg.payload));
      break;
    case 'disconnect':
      reduxStore.dispatch(disconnect());
      break;
    default:
  }
}


export default function setSocket (incomingSocket) {
  socket = incomingSocket;
}
