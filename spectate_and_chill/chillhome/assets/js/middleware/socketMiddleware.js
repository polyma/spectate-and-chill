var Constants = require('../constants/ServerConstants');
var socket = null;
import {disconnect, newSocket, receiveEvents} from '../actions/SocketActionCreators';

/*
  REDUX MIDDLEWARE
*/
export function socketMiddleware(store) {
  return next => action => {
    const result = next(action);
    if(action.type ===  Constants.ActionTypes.NEW_SOCKET_CONNECTION) {
      console.log('Registered new socket connection with middleware');
      setSocket(action.socket);
      return result;
    }
    backendSwitch(action, store);
    return result;
  };
}

/*
  Switch for events from the backend
*/

export function backendSwitch(action, store) {
  switch(action.event) {
    case Constants.ActionTypes.SOCKET_MESSAGE:
    console.log('backend message!', action);
      store.dispatch(receiveEvents(action.payload)); //assume that we ONLY have the streams that are relevant to us
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
