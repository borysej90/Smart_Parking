//create color variables 
red = "#ff6666";
green = "#77e196";

//create Url variable
Url = "http://127.0.0.1:8000/api/sites/1/lots/";

//create data and lots variables
data = [];
lots = [];

//set lots/divs on place
window.onload = function () {
    //create request
    var xhttp = new XMLHttpRequest();
    xhttp.responseType = "json";

    xhttp.onreadystatechange = function() {
    //check request status
    if (this.readyState == 4 && this.status == 200) {
        data = this.response;
        
        //create array of divs/lots
        lots.length = data.length;
        
        for (var i = 0; i < data.length; i++) {
            //create div/lot
            lots[i] = document.createElement("div");
    
            //append div/lot to body
            document.body.appendChild(lots[i]);
    
            //set lot id
            lots[i].setAttribute("id", data[i].id);

            //place div/lot on possition
            lots[i].style.position = "absolute";
            lots[i].style.left = data[i].coordinates[0] + 'px';
            lots[i].style.top = data[i].coordinates[1] + 'px'; 

            //check if slot for disabled persons 
            if (data[i].is_for_disabled == false) {
                lots[i].className="slot";
            }
            else{
                //img for slots for_disabled persons
                img = document.createElement("img"); 
                img.src = "images/logo_black.png";
                img.className = "img_prop";

                lots[i].className="slot_for_disabled";
                lots[i].appendChild(img);
            }     
        }
      }
    };
    //open request
    xhttp.open("GET", Url, true);
    //send request
    xhttp.send();
}


//func for get request
function getColor(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.responseType = "json";
    xmlHttp.open( "GET", Url); 
    xmlHttp.send();
    xmlHttp.onload = function() {        
            data = xmlHttp.response;
    };
}

function ChangeColor(x) {
    //send request to see if something changed
    getColor(Url);
    
    //change color if lot is occupied
    for (var i = 0; i < data.length; i++) {
        if (data[i].is_occupied == true) {
            lots[i].style.backgroundColor = red;
        }
        else{
            lots[i].style.backgroundColor = green;
        }
    }
    
}   
//call ChangeColor function every second
setInterval(ChangeColor, 1000);

