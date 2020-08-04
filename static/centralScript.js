document.addEventListener("DOMContentLoaded", retrieveData, false);
document.addEventListener("DOMContentLoaded", attachAssociationListener, false);
document.addEventListener("DOMContentLoaded", attachRightClicks, false);

function rightClick(ev) {
	ev.preventDefault();
	alert("Right click");
}

function retrieveData() {
		console.log("Retrieving data...");
		var obj = document.getElementById("associations-embed");
		var doc = obj.contentDocument; // get the inner DOM
	setTimeout(function() {
		if(doc!=null && doc!=undefined) {
			var el = doc.getElementById("sendData"); // assuming the embedded document has such an element
			el.addEventListener("click", sendData, false);
			console.log("Added event listener");
		}
		else {
			retrieveData();
		}
	}, 500);
}

function attachRightClicks() {
	attachRightClicksXSD();
	attachRightClicksOnto();
}

function attachRightClicksXSD() {
	var xsdE = document.getElementById("xsd-embed");
	var doc = xsdE.contentDocument; // get the inner DOM
	
	setTimeout(function() {
		if(doc!=undefined && doc!=null) {
			let allTS = doc.querySelectorAll("tspan");
			setTimeout(function() {
				if(allTS.length > 0) {
					for(let i=0; i<allTS.length; ++i) {
				allTS[i].addEventListener("contextmenu", xsdRC, false);	
			}
				}
				else {
					attachRightClicksXSD();
				}
			}, 500);
	
			
			console.log("Attached right clicks to standard nodes");
		}
		else {
			attachRightClicksXSD();			
		};
	}, 500);	
}


function attachRightClicksOnto() {
	var ontoE = document.getElementById("ontology-embed");
	var doc = ontoE.contentDocument; // get the inner DOM
	let numberShapes = 0;

	setTimeout(function() {
		if(doc!=undefined && doc!=null) {
			let allShapes = doc.querySelectorAll("circle, rect");
			setTimeout(function() {
				console.log("There are " + allShapes.length + " shapes");
				if(numberShapes < allShapes.length) { // there are new nodes
					for(let i=0; i<allShapes.length; ++i) {
							allShapes[i].addEventListener("contextmenu", ontoRC, false);	
					}
					numberShapes = allShapes.length;
					attachRightClicksOnto(); // keep checking
				}
				else {
					attachRightClicksOnto();
				}
			}, 1000);
			
			console.log("Attached right clicks to ontology nodes");
		}
		else {
			attachRightClicksOnto();			
		};
	}, 500);
	
	
}



function createRMenu(ev, currentString) {
	alert(currentString);
	let newDiv = document.createElement("div");
	newDiv.className = "right-menu";
	newDiv.style.top = ev.clientY;
	newDiv.style.left = ev.clientX;
	newDiv.style.position = "absolute";
	let listElems = document.createElement("ul");	
	let liInfo = document.createElement("li");
	liInfo.innerHTML = currentString;
	let liExit = document.createElement("li");
	liExit.innerHTML = "Exit";
	listElems.appendChild(liInfo);
	listElems.appendChild(liExit);
	newDiv.appendChild(listElems);
	
	document.body.appendChild(newDiv);


	
}

function xsdRC(ev) {
	let currentString = this.innerHTML;
	if(currentString.startsWith("name")) {
		currentString = currentString.replace(/name="/gi, "").replace(/"/gi, "");
		createRMenu(ev, currentString);
	}
	else {
		createRMenu(ev, currentString);
	}
	ev.preventDefault();
}

function ontoRC(ev) {
	alert("Right click on Ontology");
	ev.preventDefault();
}

function attachAssociationListener() {

		console.log("Retrieving data...");
		var obj = document.getElementById("associations-embed");
		var doc = obj.contentDocument; // get the inner DOM

	setTimeout(function() {
		if(doc!=null && doc!=undefined) {
			var el = doc.getElementById("locateAssociation"); // assuming the embedded document has such an element
			el.addEventListener("click", showAssociationOnGraph, false);
			console.log("Attached association listeners");
		} else {
			attachAssociationListener();
		}
	
	}, 500);
}

function sendData() {

		var obj = document.getElementById("associations-embed");
		var doc = obj.contentDocument; // get the inner DOM

	//let allRows = document.querySelectorAll("table tr");
	let stdCells = doc.querySelectorAll("table tr");
	let ontCells = doc.querySelectorAll("table tr");
	

	let stdValues = [];
	let ontValues = [];

	for(let i=1; i<stdCells.length; ++i) {
		let stdCell = stdCells[i].childNodes[0].firstChild;
		let stdCellValue = stdCell.options[stdCell.selectedIndex].text;
		if(stdValues.includes(stdCellValue)) {
			stdCell.parentNode.style.backgroundColor = "red";
		}
		else {
			stdCell.parentNode.style.backgroundColor = "green";
		}
		stdValues.push(stdCellValue);
	}

	for(let i=1; i<ontCells.length; ++i) {
		let ontCell = ontCells[i].childNodes[1].firstChild;
		let ontCellValue = ontCell.options[ontCell.selectedIndex].text;
		if(ontValues.includes(ontCellValue)) {
			ontCell.parentNode.style.backgroundColor = "red";
		}
		else {
			ontCell.parentNode.style.backgroundColor = "green";
		}
		ontValues.push(ontCellValue);
	}
}

function showAssociationOnGraph() {
	let source = this.parentNode.parentNode.parentNode.querySelectorAll(".selectedRow td select")[0];
	let destination = this.parentNode.parentNode.parentNode.querySelectorAll(".selectedRow td select")[1];

	source = source.options[source.selectedIndex].text;
	destination = destination.options[destination.selectedIndex].text;
	
	var obj = document.getElementById("xsd-embed");
	var doc = obj.contentDocument;
	var searchBoxXSD = doc.getElementById("searchTerm");
	
	searchBoxXSD.value = source;

	var evt = document.createEvent("HTMLEvents"); 
        evt.initEvent("change", false, true); // adding this created a magic and passes it as if keypressed
        searchBoxXSD.dispatchEvent(evt);

	var objOnt = document.getElementById("ontology-embed");
	var docOnt = objOnt.contentDocument;

	var degreeCollapsing = docOnt.querySelector(".distanceSliderContainer .value").innerHTML;
	console.log(degreeCollapsing);
	if(degreeCollapsing != "0") {
		var resetButton = docOnt.getElementById("reset-button");
		var clickReset = document.createEvent("HTMLEvents"); 
		clickReset.initEvent("click", false, true);
		resetButton.dispatchEvent(clickReset);
	}

	var searchBoxOnt = docOnt.getElementById("search-input-text");
	searchBoxOnt.value = destination;


	var pauseMovement = docOnt.getElementById("pause-button");
	if(pauseMovement.className != "paused highlighted") {
		setTimeout(function() {
			var clickPause = document.createEvent("HTMLEvents");
			clickPause.initEvent("click", false, true);
			pauseMovement.dispatchEvent(clickPause);
		}, 1000);
	}

	var changeSearchField = document.createEvent("HTMLEvents");
	changeSearchField.initEvent("input", false, true);
	searchBoxOnt.dispatchEvent(changeSearchField);

	var selectionDBEntry = docOnt.getElementsByClassName("dbEntry")[0];
	var clickDBEntry = document.createEvent("HTMLEvents");
	clickDBEntry.initEvent("click", false, true);
	selectionDBEntry.dispatchEvent(clickDBEntry);

	var locationSR = docOnt.getElementById("locateSearchResult");
	var clickLocate = document.createEvent("HTMLEvents");
	clickLocate.initEvent("click", false, true);
	locationSR.dispatchEvent(clickLocate);
/*
	var evtOnt = document.createEvent("HTMLEvents"); 
        evtOnt.initEvent("change", false, true); // adding this created a magic and passes it as if keypressed
        searchBoxOnt.dispatchEvent(evtOnt);*/

}
