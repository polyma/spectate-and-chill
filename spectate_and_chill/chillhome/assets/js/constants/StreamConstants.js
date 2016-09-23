var keyMirror = require('keymirror');

module.exports = {

  ActionTypes: keyMirror({
    RAW_UPDATES: null,
    ONLINE_UPDATES: null,
    REQUEST_RECOMMENDATIONS: null,
    TOP_STREAM: null,
  }),

  ErrorTypes: keyMirror({
  }),

};
