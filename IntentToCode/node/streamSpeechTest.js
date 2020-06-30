
// [START speech_streaming_mic_recognize]
const record = require('node-record-lpcm16');

// Imports the Google Cloud client library
const Speech = require('@google-cloud/speech');

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
    .on('data', (data) => console.log(data.results));

// Start recording and send the microphone input to the Speech API
record.start({
    sampleRate: sampleRate,
    threshold: 0
}).pipe(recognizeStream);

console.log('Listening, press Ctrl+C to stop.');
  // [END speech_streaming_mic_recognize]