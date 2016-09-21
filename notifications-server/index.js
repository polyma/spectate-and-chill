var Redis = require('ioredis');
var redis = new Redis(process.env.REDIS_URI);
var app = require('express')();
var http = require('http').Server(app);

app.get('/', function(req, res){
  redis.get('hi', function(err, result) {
    res.send('<h1>' + result + '</h1>');
  });
});

http.listen(process.env.PORT, function(){
  console.log('listening on *:' + process.env.PORT);
});

redis.set('hi', 'test');
