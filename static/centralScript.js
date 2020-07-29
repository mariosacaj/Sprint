document.addEventListener("DOMContentLoaded", retrieveData, false);
document.addEventListener("DOMContentLoaded", attachAssociationListener, false);

function retrieveData() {
		console.log("Retrieving data...");
		var obj = document.getElementById("associations-embed");
		var doc = obj.contentDocument; // get the inner DOM
	setTimeout(function() {
		var el = doc.getElementById("sendData"); // assuming the embedded document has such an element
		if(el!=null && el!=undefined) {
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
		var allAssociations = doc.querySelectorAll("li");
		if(allAssociations.length!=0) {
			for(let i=0; i<allAssociations.length; ++i) {
				allAssociations[i].addEventListener("click", showAssociationOnGraph, false);
			}
			console.log("Attached association listeners");
		} else {
			attachAssociationListener();
		}
	
	}, 500);
}

function sendData() {
	alert("OK");
}

function showAssociationOnGraph() {
	let source = this.getElementsByClassName("source")[0].innerHTML;
	let destination = this.getElementsByClassName("destination")[0].innerHTML;
	
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
