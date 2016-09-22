var keyMirror = require('keymirror');

module.exports = {

  ActionTypes: keyMirror({
    NEW_SOCKET_CONNECTION: null,
    DISCONNECT_SERVER: null,
    JOIN_STREAM: null,
  }),

  ErrorTypes: keyMirror({
    CONNECT_TIMEOUT: null,
  }),

};
