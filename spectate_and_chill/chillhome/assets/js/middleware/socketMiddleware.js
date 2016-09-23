var Constants = require('../constants/ServerConstants');
var socket = null;
import {receiveStreams, disconnect, newSocket} from '../actions/SocketActionCreators';


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
    if (socket) {
      backendSwitch(action);
    }

    return result;
  };
}

/*
  Switch for events from the backend
*/

var store = require('../store');
export function backendSwitch(msg) {
  switch(msg.event) {
    case 'streams':
      store.dispatch(receiveStreams(msg.payload)); //assume that we ONLY have the streams that are relevant to us
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
