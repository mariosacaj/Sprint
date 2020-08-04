document.addEventListener("DOMContentLoaded", retrieveData, false);
document.addEventListener("DOMContentLoaded", attachAssociationListener, false);

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
