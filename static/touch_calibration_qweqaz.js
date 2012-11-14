var surface = document.getElementById("my_canvas");
var ctx = surface.getContext("2d");
var img = document.getElementById("keyboard");
ctx.drawImage(img, 0, 0, 800, 276);

var letter_data = [];
var letter_area = [];

var characters_checked = ['q', 'w', 'e', 'q', 'a', 'z'];

alert("Please press the 'q', 'w', and 'e' keys in that order, then 'q', 'a', and 'z'.");


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

function start_swipe(evt){
    letter_area = []
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
    var letter = characters_checked.splice(0, 1); 
    // letter area at this point has been populated with all the x, y, timestamp info
    // from start through all the moves.
    var calibrated_letter = [letter, letter_area];
    letter_data.push(calibrated_letter);
    console.log(letter_data)
    if (characters_checked.length === 0){
        alert("Thanks! We've calibrated the keyboard for you.")
        for_charles = JSON.stringify(letter_data);
        send_json_file = $.ajax({
            type: 'POST',
            url: '/your_calibrations',
            data: {'data': for_charles},
            success: function(){
                window.location.href = ("/");
            }
        });
        }

    // prints the x, y, and timestamp data for letter area to the HTML.
    // for (var i=0; i < letter_area.length; i++) {
    //     document.getElementById("results").insertAdjacentHTML("afterbegin", "<p>X-coord: " +\
    //     letter_area[i].x +  " Y-coord: " + letter_area[i].y + " Time: " + letter_area[i].timestamp + "</p>");

}

