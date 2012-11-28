
var swipe_info = [];
var surface = document.getElementById("my_canvas");
var ctx = surface.getContext("2d");
var img = document.getElementById("keyboard");
ctx.drawImage(img, 0, 0, 800, 276);


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

function start_swipe(evt){
    ctx = surface.getContext("2d");

    evt.preventDefault();
    point_data = normalize(evt.targetTouches[0], evt.timeStamp)

    swipe_info.push(point_data);

    ctx.clearRect(0, 0, 800, 276);
    ctx.drawImage(img, 0, 0, 800, 276);

    ctx.beginPath();
    ctx.moveTo(point_data.x, point_data.y);    
}

function move(evt){
    evt.preventDefault();
    // point_data = {'x':evt['touches'][0]['clientX'], 'y':evt['touches'][0]['clientY'], 'timeStamp':evt['timeStamp']};
    point_data = normalize(evt.targetTouches[0], evt.timeStamp)

    swipe_info.push(point_data);

    ctx.lineWidth="4";
    ctx.strokeStyle = "#00FF00";

    ctx.lineTo(point_data.x, point_data.y);
    ctx.stroke();
}

function end_swipe(evt){
    evt.preventDefault();
    ctx.closePath();

    // for (var i=0; i < swipe_info.length; i++) {
    //  document.getElementById("results").insertAdjacentHTML("afterbegin", "<p>X-coord: " + swipe_info[i].x + " Y-coord: " + swipe_info[i].y + " Time: " + swipe_info[i].timestamp + "</p>");
    // }

    send_json_file = $.ajax({
        type: 'POST',
        url: '/your_swipe',
        data: {'data': JSON.stringify(swipe_info)},
        success: function(swipe_and_word_from_python, textStatus, jqXHR){
            swipe_and_word_from_python = eval(swipe_and_word_from_python);            
            swipe_points = swipe_and_word_from_python[1];
            word = swipe_and_word_from_python[0]
            document.getElementById('swipe_results').style.display = '';
            document.getElementById('word').insertAdjacentHTML("afterbegin", word);
            draw_swipe = drawDataPoints(swipe_points);
        }
    });

}
function drawDataPoints(swipe_dictionary_smoothed){
    var surface = document.getElementById("my_canvas");
    var ctx = surface.getContext("2d");
    var img = document.getElementById("keyboard");
    ctx.clearRect(0, 0, 800, 276);

    ctx.drawImage(img, 0, 0, 800, 276);
    alert("These are the points we've collected from your swipe")
    ctx.beginPath();

    for (var i=0; i < swipe_dictionary_smoothed.length; i++){
        point = swipe_dictionary_smoothed[i]
        // console.log(point.x);
        ctx.moveTo(point.x, point.y);  
        ctx.arc(point.x, point.y, 2, 0, Math.PI*2, true);
        ctx.fill();
    }
    ctx.closePath();

}


surface.addEventListener("touchstart", start_swipe, false);

surface.addEventListener("touchmove", move, false);

surface.addEventListener("touchend", end_swipe, false);

