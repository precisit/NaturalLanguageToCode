var getUserMedia = require('get-user-media-promise');

var services = require('./js/grpc-services_pb');
var grpc_web = require('grpc-web-client');

var recordMicImg = "https://www.google.com/intl/en/chrome/assets/common/images/content/mic-animate.gif"
var orginalMicImg = "http://i.imgur.com/cHidSVu.gif"

var rec_config = new services.RecognitionConfig({
    "encoding" : 0,
    "sample_rate" : 16000,
    "language_code" : "en-US",

});
var stream_config = new services.StreamingRecognitionConfig({
    "config" : rec_config,
    "single_utterance" : true,

});

window.onload = function () {
    document.getElementById("mic-img").addEventListener("click", makegrpcRequest, false);
}

function makegrpcRequest() {

    var stream_request = new services.StreamingRecognizeRequest();

    stream_request.setStreamingConfig(stream_config);

    grpc_web.grpc.invoke(services.StreamingRecognize, {
        request: stream_request,
        host: "speech.googleapis.com",
        onHeaders: function (headers) {
        },
        onMessage: function (message) {
        },
        onError: function (err) {
        },
        onComplete: function (code, msg, trailers) {
        }
    });


}



function startStream() {
    getUserMedia({ video: false, audio: true })
        .then(function (stream) {
            // TODO: Send stream to the API
            //stream.pipe(recognizeStream)
        })
        .catch(function (error) {
            console.log(error);
        });
}

function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", theUrl, true); // true = asynchronous 

    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlHttp.responseType = "json"

    document.getElementById('generatedCode').innerHTML = "<center><i>Processing...</i></center>"

    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == XMLHttpRequest.DONE && xmlHttp.status == 200) {
            if (xmlHttp.response["code"] != "") {
                callback(xmlHttp.response["code"]);
            }
            else {
                document.getElementById('generatedCode').innerHTML = "Could not understand the instruction."
            }

        }

    }

    xmlHttp.send("appro=" + document.getElementById('appro').value + "&data=" + document.getElementById('transcript').value);
}

function displayCode(responseText) {
    document.getElementById('generatedCode').innerHTML = responseText.replace(/\n/g, "<br />").replace(/\t/g, "&emsp;");
}