

var swipe_info = [];
var surface = document.getElementById("my_canvas");
var ctx = surface.getContext("2d");
var img = document.getElementById("keyboard");
ctx.drawImage(img, 0, 0, 800, 276);

function normalize(touch, timestamp) {
    var x_delta = touch.target.offsetLeft;
    var y_delta = touch.target.offsetTop;
    console.log(timestamp);
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
    console.log(evt);
    // point_data = {'x':evt['touches'][0]['clientX'], 'y':evt['touches'][0]['clientY'], 'timeStamp':evt['timeStamp']};
    point_data = normalize(evt.targetTouches[0], evt.timeStamp)

    swipe_info.push(point_data);

    ctx.clearRect(0, 0, 800, 276);
    ctx.drawImage(img, 0, 0, 800, 276);

    // last_point = {x: touch.clientX, y: touch.clientY};
    ctx.beginPath();
    ctx.moveTo(point_data.x, point_data.y);
    // ctx.fillRect(point_data.x-2, point_data.x-2, 4, 4);
    
}

function move(evt){
    evt.preventDefault();
    // point_data = {'x':evt['touches'][0]['clientX'], 'y':evt['touches'][0]['clientY'], 'timeStamp':evt['timeStamp']};
    point_data = normalize(evt.targetTouches[0], evt.timeStamp)

    swipe_info.push(point_data);
    // touches = evt.targetTouches;
    // touch = touches[0];
    ctx.lineWidth="4";
    ctx.strokeStyle = "#00FF00";
    // ctx.moveTo(previous_point.x, previous_point.y);

    // ctx.moveTo(touch.clientX, touch.clientY);

    ctx.lineTo(point_data.x, point_data.y);

    // ctx.lineTo(point_data.x, point_data.y);
    ctx.stroke();
}

function end_swipe(evt){
    evt.preventDefault();
    ctx.closePath();

    for (var i=0; i < swipe_info.length; i++) {
     document.getElementById("results").insertAdjacentHTML("afterbegin", "<p>X-coord: " + swipe_info[i].x + " Y-coord: " + swipe_info[i].y + " Time: " + swipe_info[i].timestamp + "</p>");
    }

    send_json_file = $.ajax({
        type: 'POST',
        url: '/your_swipe',
        data: {'data': JSON.stringify(swipe_info)},
        success: function(){
            console.log('Data stringified');
        }
    });

}

surface.addEventListener("touchstart", start_swipe, false);

surface.addEventListener("touchmove", move, false);

surface.addEventListener("touchend", end_swipe, false);

