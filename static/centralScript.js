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

function addItemToMenu(menuList, stringInMenu, menuDiv, attachedFunction) {
	let liInfo = document.createElement("li");
	liInfo.innerHTML = stringInMenu;
	liInfo.addEventListener("click", attachedFunction, false);
	menuList.appendChild(liInfo);
	return menuList;
}

function addTitleToMenu(menuList, titleMenu, menuDiv) {
	let liTitle = document.createElement("li");
	liTitle.className = "menu-title";
	liTitle.innerHTML = titleMenu;
	menuList.appendChild(liTitle);
	return menuList;
}

function addCloseToMenu(menuList, labelClose, menuDiv) {
	let liClose = document.createElement("li");
	liClose.className = "menu-close";
	liClose.innerHTML = labelClose;
	liClose.addEventListener("click", closeMenu, false);
	menuList.appendChild(liClose);
	return menuList;
}

function closeMenu() {
	let allMenus = document.querySelectorAll(".right-menu");
	for(let i=0; i<allMenus.length; ++i) {
		allMenus[i].remove();
	}
}

function createRMenu(ev, currentString, startingType) {
	let allRM = document.querySelectorAll(".right-menu");
	for(let i=0; i<allRM.length; ++i) {
		allRM[i].remove();
	}
	let newDiv = document.createElement("div");
	newDiv.className = "right-menu";
	let listElems = document.createElement("ul");	
	
	listElems = addTitleToMenu(listElems, "Options", newDiv);
	listElems = addItemToMenu(listElems, '<span class="origin">Term</span><br/><span>' + currentString + '</span>');
	listElems = addItemToMenu(listElems, '<span class="associatedTo">Associated to</span><br/><span>' + findAssociation(currentString, startingType) + '</span>', newDiv);

	listElems = addItemToMenu(listElems, "Add to association", newDiv, addToAssociation.bind(ev, currentString, startingType));

	listElems = addItemToMenu(listElems, "Remove association", newDiv, removeAssociation.bind(ev, currentString, startingType));

	listElems = addCloseToMenu(listElems, "Close menu", newDiv);

	newDiv.appendChild(listElems);
	document.body.appendChild(newDiv);
}

function addToAssociation(startingString, startingType) {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let rows = doc.querySelectorAll("table tr");	
	
	var startingColumn = undefined;

	if(startingType == "XSD") {
		startingColumn = 0;
	}
	else if(startingType == "Ontology") {
		startingColumn = 1;
	}

	let otherColumn = Math.abs(startingColumn - 1);
	let alreadyInserted = false;

	for(let i=1; i<rows.length; ++i) {
		let startingSelector = rows[i].childNodes[startingColumn].firstChild;
		let startingValue = undefined;
		if(startingSelector.innerHTML.startsWith("<select>")) {
		startingValue = startingSelector.options[startingSelector.selectedIndex].text;
		}
		else {
			startingValue = startingSelector.firstChild.innerHTML;
		}
		if(startingValue == startingString) {
			alert("The value has already been inserted");
			alreadyInserted = true;
		}
	}
	
	if(alreadyInserted == false) {
		dispatchAddAssociation(doc);
		if(startingType == "XSD") {
			chooseStd(startingString, doc.querySelectorAll("table tr"));
		}	
		else if(startingType == "Ontology") {
			chooseOntology(startingString, doc.querySelectorAll("table tr"));
		}	
	}
}

function chooseStd(value, trs) {
	let lastRow = trs[trs.length - 1];
	let stdSel = lastRow.childNodes[0].firstChild;
	stdSel.parentNode.innerHTML = "<span>" + value + "</span>";
}

function chooseOntology(value, trs) {
	let lastRow = trs[trs.length - 1];
	let ontSel = lastRow.childNodes[1].firstChild;
	ontSel.parentNode.innerHTML = "<span>" + value + "</span>";
}

function dispatchAddAssociation(doc) {
	var evt = document.createEvent("HTMLEvents"); 
	evt.initEvent("click", false, true);
	doc.getElementById("addAssociation").dispatchEvent(evt);
}

function removeAssociation(startingString, startingType) {
	alert("REMOVE " + startingString + ", " + startingType);
}


function findAssociation(currentString, startingType) {
	if(startingType == "XSD") {
		return findAssociationGivenXSD(currentString);
	}
	else if(startingType == "Ontology") {
		return findAssociationGivenOntology(currentString);
	}
}

function findAssociationGivenXSD(currentString) {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let rows = doc.querySelectorAll("table tr");	
	for(let i=1; i<rows.length; ++i) {
		let xsdSelector = rows[i].childNodes[0].firstChild;
		let xsdValue = undefined;
		if(xsdSelector.innerHTML.startsWith("<select>")) {
			xsdValue = xsdSelector.options[xsdSelector.selectedIndex].text;
		}
		else {
			xsdValue = xsdSelector.firstChild.innerHTML;
		}
		
		if(xsdValue == currentString) {
			let ontologySelector = rows[i].childNodes[1].firstChild;
			let ontologyValue = ontologySelector.options[ontologySelector.selectedIndex].text;
			return ontologyValue;
		}
	}
	return "-";
}

function findAssociationGivenOntology(currentString) {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let rows = doc.querySelectorAll("table tr");	
	for(let i=1; i<rows.length; ++i) {
		let ontoSelector = rows[i].childNodes[1].firstChild;

		let ontoValue = undefined;
		if(ontoSelector.innerHTML.startsWith("<select>")) {
			ontoValue = ontoSelector.options[ontoSelector.selectedIndex].text;
		}
		else {
			ontoValue = ontoSelector.firstChild.innerHTML;
		}

		// let ontoValue = ontoSelector.options[ontoSelector.selectedIndex].text;
		if(ontoValue == currentString) {
			let xsdSelector = rows[i].childNodes[0].firstChild;
			let xsdValue = xsdSelector.options[xsdSelector.selectedIndex].text;
			return xsdValue;
		}
	}
	return "-";	
}

function xsdRC(ev) {
	let currentString = this.innerHTML;
	if(currentString.startsWith("name")) {
		currentString = currentString.replace(/name="/gi, "").replace(/"/gi, "");
		createRMenu(ev, currentString, "XSD");
	}
	else {
		createRMenu(ev, currentString, "XSD");
	}
	ev.preventDefault();
}

function ontoRC(ev) {
	let currentString = this.querySelector("title").innerHTML;
	createRMenu(ev, currentString, "Ontology");
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

function getSelection(cell) {
	if(cell.innerHTML.startsWith("<option>")) {
		return cell.options[cell.selectedIndex].text;
	}
	else {
		return cell.innerHTML;	
	}
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
		let stdCellValue = getSelection(stdCell);

		if(stdValues.includes(stdCellValue)) {
			stdCell.parentNode.style.backgroundColor = "rgb(255, 153, 153)";
		}
		else {
			stdCell.parentNode.style.backgroundColor = "rgb(153, 255, 51)";
		}
		stdValues.push(stdCellValue);
	}

	for(let i=1; i<ontCells.length; ++i) {
		let ontCell = ontCells[i].childNodes[1].firstChild;
		let ontCellValue = getSelection(ontCell);

		if(ontValues.includes(ontCellValue)) {
			ontCell.parentNode.style.backgroundColor = "rgb(255, 153, 153)";
		}
		else {
			ontCell.parentNode.style.backgroundColor = "rgb(153, 255, 51)";
		}
		ontValues.push(ontCellValue);
	}
}

function showAssociationOnGraph() {
	let source = this.parentNode.parentNode.parentNode.querySelectorAll(".selectedRow td")[0];
	let destination = this.parentNode.parentNode.parentNode.querySelectorAll(".selectedRow td")[1];

	source = getSelection(source.firstChild);
	destination = getSelection(destination.firstChild);

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

}
