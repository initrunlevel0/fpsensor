var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use('/static', express.static(__dirname + '/static'))
app.listen(3000);

app.get('/', function(req, res) {
    // Server app.html
    fs.readFile('./app.html', function(err, data) {
        res.end(data);
    });
});


// UDP Broadcast stuff
var dgram = require('dgram');
var port = 5000;
var host = "192.168.43.255";    // Receive and send from/to everything
var socket = dgram.createSocket('udp4');
var receivedData = {};

socket.on('message', function(message, remote) {
    console.log('Receiving data: ' + message.toString());
    try {
        receivedData = JSON.parse(message.toString());
    } catch (ex) {

    }
});

socket.bind(port, host);

app.get('/data', function(req, res) {
    // TODO: Fuzzy
    res.send(receivedData);
});


// Unimplemented, POST from UDP broadcast instead
//app.post('/data', function(req, res) {
//});




