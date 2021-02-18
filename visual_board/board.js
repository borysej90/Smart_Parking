red = "rgb(75, 13, 13)";
green = "rgb(12, 56, 12)";

counter = 6;


function changeColor(x) {
    slot = document.getElementById(x);
    if (slot.style.backgroundColor == red) {
        slot.style.backgroundColor = green; 
        counter++;
    }
    else{
        slot.style.backgroundColor = red;
        counter--;
    }
    return false;
}   

setInterval(function(){
    document.getElementById("count").innerHTML = counter;
}, 10); // 1000 м.сек

