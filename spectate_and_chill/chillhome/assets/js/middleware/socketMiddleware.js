var Constants = require('../constants/ServerConstants');
var socket = null;



export function socketMiddleware(store) {
  return next => action => {
    const result = next(action);
    if(action.type ===  Constants.ActionTypes.NEW_SOCKET_CONNECTION) {
      console.log('Registered new socket connection with middleware');
      setSocket(action.socket);
      return result;
    }
    if (socket) {
      frontendSwitch(action);
    }

    return result;
  };
}

/*
  Switch for events from the backend
*/
import {setOwnerStreaming, userUpdate, receiveMessage, disconnect} from '../actions/ChatServerActionCreators';
var reduxStore = require('../store');
export function backendSwitch(msg) {
  switch(msg.event) {
    case 'msg':
      reduxStore.dispatch(receiveMessage(msg.payload));
      break;
    case 'user-store-update':
      reduxStore.dispatch(userUpdate(msg.payload));
      break;
    case 'stream-id':
      reduxStore.dispatch(setOwnerStreaming(msg.payload));
      break;
    case 'disconnect':
      reduxStore.dispatch(disconnect());
      break;
    default:
  }
}

/*
  Switch for actions created by the front-end
*/
function frontendSwitch(action) {
  console.log('frontend', action);
  switch(action.type) {
    case Constants.ActionTypes.JOIN_STREAM:
      socket.send({
        event: 'connect',
        payload: action.streamId,
      });
      break;
    default:
  }
}


export default function setSocket (incomingSocket) {
  socket = incomingSocket;
}
