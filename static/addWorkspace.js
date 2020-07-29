document.addEventListener("DOMContentLoaded", associateAllActions, false);
document.addEventListener("DOMContentLoaded", resizeAll, false);
document.getElementById("dialog-ontology").addEventListener("mousemove", resizeAll, false);
document.getElementById("dialog-xsd").addEventListener("mousemove", resizeAll, false);
document.getElementById("dialog-associations").addEventListener("mousemove", resizeAll, false);

function associateAllActions() {
	associateActions("dialog-ontology");
	associateActions("dialog-xsd");
	associateActions("dialog-associations");
}

function resizeAll() {
	document.querySelector("#dialog-ontology #ontology-embed").style.height = parseInt(document.querySelector("#dialog-ontology").style.height.split("px")[0] - 32).toString() + "px";
document.querySelector("#dialog-ontology #ontology-embed").style.width = document.querySelector("#dialog-ontology").style.width;


	document.querySelector("#dialog-xsd #xsd-embed").style.height = parseInt(document.querySelector("#dialog-xsd").style.height.split("px")[0] - 32).toString() + "px";
document.querySelector("#dialog-xsd #xsd-embed").style.width = document.querySelector("#dialog-xsd").style.width;


	document.querySelector("#dialog-associations #associations-embed").style.height = parseInt(document.querySelector("#dialog-associations").style.height.split("px")[0] - 32).toString() + "px";
document.querySelector("#dialog-associations #associations-embed").style.width = document.querySelector("#dialog-associations").style.width;
}

function associateActions(dialogID) {
	dialogDiv = document.getElementById(dialogID);
closeButton = document.querySelector("#" + dialogID + " .close");
minimizeButton = document.querySelector("#" + dialogID + " .minimize");
  dragElement(dialogDiv);
  dialogDiv.addEventListener("click", activateFocus);
  closeButton.addEventListener("click", closeWindow);
  minimizeButton.addEventListener("click", minimizeWindow);  
}

function closeWindow() {
  this.parentNode.remove();
}

function minimizeWindow() {
  let dialogBox = this.parentNode;
  if(dialogBox.style.resize === "none") {
    dialogBox.style.height = "40vh";
    dialogBox.style.width = "40vw";
    dialogBox.style.overflow = "scroll";
    dialogBox.style.resize = "both";
  }
  else {
    dialogBox.style.height = "32px";
    dialogBox.style.width = "256px";
    dialogBox.style.overflow = "hidden";
    dialogBox.style.resize = "none";
  }
}



function activateFocus() {
  let zIndexMax = 0;
  for(var i=0; i<document.querySelectorAll(".dialog").length; ++i) {
    if(parseInt(document.querySelectorAll(".dialog")[i].style.zIndex) > zIndexMax) {
        zIndexMax = parseInt(document.querySelectorAll(".dialog")[i].style.zIndex);
    }
  }
  this.style.zIndex = parseInt(zIndexMax+1);
  
  // Normalize indexes
  let zIndexMin = Number.POSITIVE_INFINITY;
  for(var i=0; i<document.querySelectorAll(".dialog").length; ++i) {
    if(parseInt(document.querySelectorAll(".dialog")[i].style.zIndex) < zIndexMin) {
        zIndexMin = parseInt(document.querySelectorAll(".dialog")[i].style.zIndex);
    }
  }
  
  for(var i=0; i<document.querySelectorAll(".dialog").length; ++i) {
         document.querySelectorAll(".dialog")[i].style.zIndex = parseInt(document.querySelectorAll(".dialog")[i].style.zIndex - zIndexMin);
  }
}

/*
 * Designed by ZulNs, @Gorontalo, Indonesia, 7 June 2017
 * Extended by FrankBuchholz, Germany, 2019
*/

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.querySelector("#"+elmnt.id + " .titlebar")) {
    // if present, the header is where you move the DIV from:
    document.querySelector("#"+elmnt.id + " .titlebar").onmousedown = dragMouseDown;
    //document.getElementById(elmnt.id + "titlebar").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = Math.max((elmnt.offsetTop - pos2), 0) + "px";
    elmnt.style.left = Math.max((elmnt.offsetLeft - pos1), 0) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}
/* */




