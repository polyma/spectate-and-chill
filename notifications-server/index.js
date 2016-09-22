var Redis = require('ioredis');
var sub = new Redis(process.env.REDIS_URI);
sub.on('connect', function(err, count) {
  console.log('connected to redis');
  sub.subscribe('event');
});
sub.on('message', function(channel, message) {
  console.log('message', message, 'received from', channel);
});
var app = require('express')();
var http = require('http').Server(app);

app.get('/', function(req, res){
    res.send('<h1>HI</h1>');
});

http.listen(process.env.PORT, function(){
  console.log('listening on *:' + process.env.PORT);
});
