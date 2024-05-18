// JS part for homepage

// initialize the index
let index = 1;
// get the elements
var prog = "Utopia For Movie Lovers";
var mt = document.getElementById("headP");
function writeText() {
    mt.innerText = prog.slice(0, index);
    // increase the index for iteration
    index++;
}
// set speed for title
setInterval(writeText, 150);