var Constants = require('../constants/ServerConstants');
var socket = null;
import {receiveStreams, disconnect, newSocket} from '../actions/SocketActionCreators';
import {dispatch} from '../store';

/*
  SET UP SOCKET CONNECTION
*/
var io = require('socket.io-client');
socket = io.connect('ws://localhost:8080'); //NOTE: need to send user id for this to work
socket.on('connect', function() {
  console.log('connected to server!');
  if(dispatch) { //store may not be present TODO: fix this...
    dispatch(newSocket(socket));
  }
  //TODO: remove this
  setUserId('21505497_euw');
});
socket.on('disconnect', function() {
  dispatch(disconnect());
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

export function backendSwitch(msg) {
  switch(msg.event) {
    case 'streams':
      dispatch(receiveStreams(msg.payload));
      break;
    // case 'disconnect':
    //   dispatch(disconnect());
    //   break;
    default:
  }
}


export default function setSocket (incomingSocket) {
  socket = incomingSocket;
}

export function setUserId(id) {
  socket.send(id);
}
