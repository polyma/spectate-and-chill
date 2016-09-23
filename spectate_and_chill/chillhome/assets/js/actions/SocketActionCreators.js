const ServerConstants = require('../constants/ServerConstants');
const StreamConstants = require('../constants/StreamConstants');


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
