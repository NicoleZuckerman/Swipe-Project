var swipe_info = []
surface = document.getElementById("keyboard")

surface.addEventListener("touchstart", function(evt) {
    evt.preventDefault();
    // here's a way to think about the data below:
    // touches = evt['touches']
    // that_first_thing = touches[0]
    // x_coord = that_first_thing['clientX']
    // y_coord = that_first_thing['clientY']

    point_data = {'x':evt['touches'][0]['clientX'], 'y':evt['touches'][0]['clientY'], 'timeStamp':evt['timeStamp']};
    swipe_info.push(point_data);
    }, false);

surface.addEventListener("touchmove", function(evt){
    evt.preventDefault();
    point_data = {'x':evt['touches'][0]['clientX'], 'y':evt['touches'][0]['clientY'], 'timeStamp':evt['timeStamp']};
    swipe_info.push(point_data);


    var ctx = surface.getContext("2d");
    ctx.lineWidth = 4;
         
    for (var i=0; i<touches.length; i++) {
    var color = colorForTouch(touches[i]);
    var idx = ongoingTouchIndexById(touches[i].identifier);
 
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(ongoingTouches[idx].pageX, ongoingTouches[idx].pageY);
    ctx.lineTo(touches[i].pageX, touches[i].pageY);
    ctx.closePath();
    ctx.stroke();
    ongoingTouches.splice(idx, 1, touches[i]);  // swap in the new touch record
    }, false);

surface.addEventListener("touchend", function(evt) {
    evt.preventDefault();

    for (var i=0; i < swipe_info.length; i++) {
     document.getElementById("results").insertAdjacentHTML("afterbegin", "<p>X-coord: " + swipe_info[i].x + " Y-coord: " + swipe_info[i].y + " Time: " + swipe_info[i].timeStamp + "</p>");
    }

    send_json_file = $.ajax({
        type: 'POST',
        url: '/your_swipe',
        data: {'data': JSON.stringify(swipe_info)},
        success: function(){
            console.log('Data stringified');
        }
    });
}, false);

