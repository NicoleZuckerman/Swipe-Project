var surface = document.getElementById("my_canvas");
var ctx = surface.getContext("2d");
var img = document.getElementById("keyboard");
ctx.drawImage(img, 0, 0, 800, 276);
// console.log(kb_data);
window.onload = function(){
    // console.log(kb_data);
    // keyboard = kb_data
    for(i=0; i<kb_data.length; i++){
        letter = kb_data[i];
        // console.log("letter is:" + letter.letter + ", the x is: " + letter.x + ", and the y is: " + letter.y);
        ctx.fillRect(letter.x-2, letter.y-2, 4, 4);

    };
}

