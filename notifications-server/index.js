'use strict';
var clients = {};
var Redis = require('ioredis');
var sub = new Redis(process.env.REDIS_URI);
sub.on('connect', function(err, count) {
  console.log('connected to redis');
  sub.subscribe('event');
});
sub.on('message', function(channel, message) {
  console.log('message', message, 'received from', channel);
  // should be an  array
  let m = JSON.parse(message)
  sendToAllClients(message);
});
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
    res.send('<h1>HI</h1>');
});
app.get('/online', function(req, res){
    sendToAllClients([
          {
            id: 'streamer',
            matchId: 0,
          },
          {
            id: 'adil',
            matchId: 1234,
          },
        ]);
});
app.get('/offline', function(req, res){
    sendToAllClients([
      {
        id: 'streamer',
        matchId: 0,
      },
      {
        id: 'adil',
        matchId: 0,
      },
    ]);
});

function sendToAllClients(objs) {
  Object.keys(clients).forEach((client) => {
    clients[client].send(objs);
  })
}

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function() {
    console.log('user', socket.id, 'disconnected');
  });


  socket.on('message', function(msg) {
    //NOTE: the only messages we receive from the frontend contain the user id that they are
    //Message containing summoner id + realm
    console.log('message received from client', msg);
    //sign up for their own channel
    socket.id = msg;
    console.log('set user socket id to', socket.id);
    clients[socket.id] = socket;
  });
});

http.listen(process.env.PORT, function(){
  console.log('listening on *:' + process.env.PORT);
});
