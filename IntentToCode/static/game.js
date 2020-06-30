var recordMicImg = "https://www.google.com/intl/en/chrome/assets/common/images/content/mic-animate.gif";
var orginalMicImg = "http://i.imgur.com/cHidSVu.gif";
var editor;

//Defining obsticles grid
var grid = [];
for (var i = 0; i < 8; i++) {
    grid[i] = [];
    for (var j = 0; j < 8; j++) {
        grid[i][j] = 1;
    }
}
//Squares where objects cannot walk
grid[3][0] = 0;
grid[3][1] = 0;
grid[3][2] = 0;
grid[3][3] = 0;
grid[3][5] = 0;
grid[3][6] = 0;
grid[3][7] = 0;

var canvas = document.getElementById("game");
var context = canvas.getContext("2d");
context.textBaseline = "middle";

// Defining Environment
var objectsToRender = []
var character = new Obj("character", false, context, 1, 1, "red");
objectsToRender.push(character);
var tree = new Obj("tree", false, context, 3, 4, "green");
objectsToRender.push(tree);
var cow = new Obj("cow", false, context, 5, 2, "pink");
objectsToRender.push(cow);
var goal = new Obj("goal", false, context, 6, 6, "red");
objectsToRender.push(goal);

var axe = new Obj("axe", true)


cow.pink = true;
character.red = true;
tree.green = true;
goal.red = true;

// If no performer of the action is given
function jump(direction) {
    character.jump(direction);
}
function cut(target, cutWith) {
    character.cut(target, cutWith);
}
function walk(direction) {
    character.walk(direction);
}
function eat(target) {
    character.eat(target);
}

update();

function update() {
    // clear canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawWater();
    drawGrid(8, 8, 64, 64);
    drawObjects();
    didIwin();
}

function didIwin() {
    if (Math.abs(character._x - goal._x) <= 1 && Math.abs(character._y - goal._y) <= 1) {
        showGameInfo(this._name, '<iframe src="https://www.youtube.com/embed/9QS0q3mGPGg?ecver=2&autoplay=1&t=25s" width="640" height="360" frameborder="0" style="position:absolute;width:100%;height:100%;left:0" allowfullscreen></iframe>');

    }
}

function drawWater() {
    context.fillStyle = "blue";
    context.fillRect(192, 0, 64, 256);
    context.fillRect(192, 320, 64, 192);
}


function drawObjects() {
    objectsToRender.forEach(function (obj) {
        obj.drawObj();
    }, this);
}

function drawGrid(boxesX, boxesY, boxWidth, boxHeight) {
    // Padding
    var p = 0;

    for (var x = 0; x <= boxWidth * boxesX; x += boxWidth) {
        context.moveTo(0.5 + x + p, p);
        context.lineTo(0.5 + x + p, boxHeight * boxesY + p);
    }
    for (var x = 0; x <= boxHeight * boxesY; x += boxWidth) {
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(boxWidth * boxesX + p, 0.5 + x + p);
    }

    context.strokeStyle = "#cccccc";
    context.stroke();
}

function drawCircle(context, posX, posY, radius, color) {
    context.beginPath();
    context.arc(posX + radius, posY + radius, radius, 0, 2 * Math.PI);
    context.fillStyle = color;
    context.fill();
}

function showGameInfo(speaker, infoString) {
    document.getElementById('gameInfo').innerHTML = "<strong>" + speaker + "</strong>: " + infoString;
}

(function () {
    // ACE editor config
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
    editor.$blockScrolling = Infinity;

    document.getElementById('mic-img').addEventListener("click", startDictation);

    function startDictation() {
        /*document.getElementById('status').innerHTML = "<center><i>Voice is on</i></center>";
         Voice to text using webkitSpeechRecognition - Low accuracy and is therefore disabled
        */
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
                // HTML5 Speech Recognition API
                var recognition = new webkitSpeechRecognition();
    
                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.lang = "en-US";
                recognition.start();
                document.getElementById('mic-img').src = recordMicImg
    
                recognition.onresult = function (e) {
                    document.getElementById('transcript').value
                        = e.results[0][0].transcript;
                    recognition.stop();
                    document.getElementById('mic-img').src = orginalMicImg
                    httpGetAsync('/getcode', displayCode);
                };
                recognition.onerror = function (e) {
                    recognition.stop();
                }
            }
    }
    function httpGetAsync(theUrl, callback) {

        if (document.getElementById('transcript').value == "") {
            return;
        }

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", theUrl, true); // true = asynchronous 

        xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlHttp.responseType = "json"

        document.getElementById('status').innerHTML = "<center><i>Processing...</i></center>"

        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState == XMLHttpRequest.DONE && xmlHttp.status == 200) {
                if (xmlHttp.response["code"] != "") {
                    callback(xmlHttp.response["code"]);
                }
                else {
                    document.getElementById('status').innerHTML = "Could not understand the instruction."
                }

            }
            if (xmlHttp.readyState == XMLHttpRequest.DONE && xmlHttp.status != 200) {
                document.getElementById('status').innerHTML = "<center><i>Server error</i></center>";
            }

        }

        xmlHttp.send("appro=" + document.getElementById('appro').value + "&data=" + document.getElementById('transcript').value);
    }

    function displayCode(responseText) {
        editor.insert(responseText);
        document.getElementById('status').innerHTML = "<center><i>Success</i></center>";
    }

    $("#form").on("submit", function () {
        httpGetAsync('/getcode', displayCode);
        return false;
    });

    $("#clear-btn").on("click", function () {
        editor.setValue("");
    });
    $("#run-btn").on("click", function () {
        var code = editor.getValue();
        try {
            eval(code);
            update();
            //editor.setValue("");
            document.getElementById('status').innerHTML = "";
        } catch (e) {
            console.error(e);
            showGameInfo("CODE ERROR", e.message);
        }
    });

})();
