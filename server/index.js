var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');
var spawn = require('child_process').spawn;

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
    var input = {};

    input.temperature = receivedData.temperature;
    input.humidity = receivedData.humidity;
    input.lightIntensity = receivedData.lightIntensity;
    input.hours = (new Date).getHours()
    input.source = receivedData.source;

    // Default received data
    // COMMENT ON REAL TEST
    if(!receivedData.temperature) input.temperature = 25.0;
    if(!receivedData.humidity) input.humidity = 70;
    if(!receivedData.lightIntensity) input.lightIntensity = 30;

    var stdout = "";
    var ps = spawn('python', ['fuzzy.py'], {cwd: '../script'});
    ps.stdin.end(JSON.stringify(input))
    ps.stderr.pipe(process.stdout);

    ps.stdout.on('data', function(data) {
        stdout += data.toString();
    });

    ps.on('close', function() {
        try {
            var output = [];
            var weather = JSON.parse(stdout);
            if(weather.hujan > 0) {
                output.push(Math.round(weather.hujan*100).toString() + "% Hujan");
            }

            if(weather.sejuk > 0) {
                output.push(Math.round(weather.sejuk*100).toString() + "% Sejuk");
            }

            if(weather.berawan > 0) {
                output.push(Math.round(weather.berawan*100).toString() + "% Berawan");
            }

            if(weather.cerah > 0) {
                output.push(Math.round(weather.cerah*100).toString() + "% Cerah");
            }

            res.send({data: input, weather: output, fuzz: weather});
        } catch (ex) {
            res.send({data: input})
        }
    });

});


// Unimplemented, POST from UDP broadcast instead
//app.post('/data', function(req, res) {
//});




