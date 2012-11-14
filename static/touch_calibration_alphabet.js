var letter_area = [];
var surface = document.getElementById("my_canvas");
var ctx = surface.getContext("2d");
var img = document.getElementById("keyboard");
ctx.drawImage(img, 0, 0, 800, 276);

num_done = []

var first_letter = calibrate(num_done.length)


function calibrate(num_of_letters_done){
    var letter = String.fromCharCode(97 + num_of_letters_done)
    alert("Please press the " + letter + " key");
}
surface.addEventListener("touchstart", start_swipe, false);
surface.addEventListener("touchmove", move, false);
surface.addEventListener("touchend", end_swipe, false);

function normalize(touch, timestamp) {
    var x_delta = touch.target.offsetLeft;
    var y_delta = touch.target.offsetTop;
    var point = {
        "x": touch.clientX-x_delta,
        "y": touch.clientY-y_delta,
        "timestamp": timestamp
    }
    return point;
}
var last_point = null;

function start_swipe(evt){
    var ctx = surface.getContext("2d");
    evt.preventDefault();
    point_data = normalize(evt.targetTouches[0], evt.timeStamp)
    letter_area.push(point_data);

    ctx.clearRect(0, 0, 800, 276);
    ctx.drawImage(img, 0, 0, 800, 276);

    ctx.beginPath();
    ctx.moveTo(point_data.x, point_data.y);    
}

function move(evt){
    evt.preventDefault();
    point_data = normalize(evt.targetTouches[0], evt.timeStamp)

    letter_area.push(point_data);
    ctx.lineWidth="4";
    ctx.strokeStyle = "#00FF00";

    ctx.lineTo(point_data.x, point_data.y);
    ctx.stroke();
}

function end_swipe(evt){
    evt.preventDefault();
    ctx.closePath();

    for (var i=0; i < letter_area.length; i++) {
     document.getElementById("results").insertAdjacentHTML("afterbegin", "<p>X-coord: " + letter_area[i].x + " Y-coord: " + letter_area[i].y + " Time: " + letter_area[i].timestamp + "</p>");
    }

    var current_letter = String.fromCharCode(97 + num_done.length);
    var calibrated_data = [current_letter, letter_area];
    num_done.push(calibrated_data);
    var go_to_next_letter = calibrate(num_done.length);
    letter_area = [];

    send_json_file = $.ajax({
        type: 'POST',
        url: '/your_calibrations',
        data: {'data': JSON.stringify(calibrated_data)},
        success: function(){
            console.log('Data stringified');
        }
        });

}

