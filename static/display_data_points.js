var surface = document.getElementById("my_canvas");
var ctx = surface.getContext("2d");
var img = document.getElementById("keyboard");
ctx.drawImage(img, 0, 0, 800, 276);
// console.log(path_data_points);
window.onload = function(){
    for(i=0; i<path_data_points.length; i++){
        point = path_data_points[i];
        // console.log("letter is:" + point.letter + ", the x is: " + point.x + ", and the y is: " + point.y)
        ctx.fillRect(point.x-2, point.y-2, 4, 4);

    }
}
