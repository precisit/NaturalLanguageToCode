var websocket = require('websocket-stream')
const Speech = require('@google-cloud/speech');
var http = require('http');
var fs = require('fs');
var server = http.createServer();
var opts = {}
opts.server = server;

function handle(stream) {
    console.log("Stream connected");
    //stream.pipe(process.stdout);
    stream.pipe(stream);
    //stream.pipe(recognizeStream);
}

websocket.createServer(opts, handle);
server.listen('8001');

// Instantiates a client
const speech = Speech();

// The encoding of the audio file, e.g. 'LINEAR16'
const encoding = 'LINEAR16';

// The sample rate of the audio file, e.g. 16000
const sampleRate = 16000;

const request = {
    config: {
        encoding: encoding,
        sampleRate: sampleRate
    }
};

// Create a recognize stream
const recognizeStream = speech.createRecognizeStream(request)
    .on('error', console.error)
    .on('data', (data) => {
        console.log("We got a respons");
        console.log(data.results);
    });
