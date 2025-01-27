document.addEventListener("DOMContentLoaded", retrieveData, false);
document.addEventListener("DOMContentLoaded", attachAssociationListener, false);
document.addEventListener("DOMContentLoaded", attachRightClicks, false);


function rightClick(ev) {
	ev.preventDefault();
}

function retrieveData() {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	setTimeout(function () {
		if (doc != null && doc != undefined) {
			var el = doc.getElementById("sendData"); // assuming the embedded document has such an element
			if (el == null) {
				retrieveData();
			}
			else {
				el.addEventListener("click", sendData, false);
			}
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

	setTimeout(function () {
		if (doc != undefined && doc != null) {

			/*doc.getElementById("compress").addEventListener("click", attachRightClicks, false);
			doc.getElementById("compress").style.display = "block";
			*/

			let allTS = doc.querySelectorAll("tspan");
			setTimeout(function () {
				if (allTS.length > 0) {
					for (let i = 0; i < allTS.length; ++i) {
						allTS[i].addEventListener("contextmenu", xsdRC, false);
						allTS[i].addEventListener("click", attachRightClicks, false);
					}
				}
				else {
					attachRightClicksXSD();
				}
			}, 500);


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

	setTimeout(function () {
		if (doc != undefined && doc != null) {
			let allShapes = doc.querySelectorAll("circle, rect");
			setTimeout(function () {
				if (numberShapes < allShapes.length) { // there are new nodes
					for (let i = 0; i < allShapes.length; ++i) {
						allShapes[i].addEventListener("contextmenu", ontoRC, false);
					}
					numberShapes = allShapes.length;
					attachRightClicksOnto(); // keep checking
				}
				else {
					attachRightClicksOnto();
				}
			}, 1000);

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
	for (let i = 0; i < allMenus.length; ++i) {
		allMenus[i].remove();
	}
}

function createRMenu(ev, currentString, startingType) {
	let allRM = document.querySelectorAll(".right-menu");

	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let selectedRow = doc.querySelector("table tr.selectedForAssociation");

	let xsdString = undefined;
	let ontoString = undefined;


	if (startingType == "XSD") {
		xsdString = currentString;
		let ontoSelector = selectedRow.querySelectorAll("td")[1];

		if (ontoSelector.innerHTML.startsWith("<select>")) {
			ontoString = ontoSelector.firstChild.options[ontoSelector.firstChild.selectedIndex].text;
		}
		else {
			ontoString = ontoSelector.firstChild.innerHTML;
		}
	}
	else {
		ontoString = currentString;

		let xsdSelector = selectedRow.querySelectorAll("td")[0];

		if (xsdSelector.innerHTML.startsWith("<select>")) {
			xsdString = xsdSelector.firstChild.options[xsdSelector.firstChild.selectedIndex].text;
		}
		else {
			xsdString = xsdSelector.firstChild.innerHTML;
		}

	}

	let validCombination = false;


	for (let i = 0; i < allRM.length; ++i) {
		allRM[i].remove();
	}
	let newDiv = document.createElement("div");
	newDiv.className = "right-menu";
	let listElems = document.createElement("ul");




	listElems = addTitleToMenu(listElems, "Options", newDiv);
	listElems = addItemToMenu(listElems, '<span class="origin">Term</span><br/><span>' + currentString + '</span>');
	//listElems = addItemToMenu(listElems, '<span class="associatedTo">Associated to</span><br/><span>' + findAssociation(currentString, startingType) + '</span>', newDiv);



	if (ontoString == "-" || xsdString == "-") {
		validCombination = true;
		listElems = addItemToMenu(listElems, "Add to association", newDiv, addToAssociation.bind(ev, currentString, startingType));

		listElems = addItemToMenu(listElems, "Remove association", newDiv, removeAssociation.bind(ev, currentString, startingType));

		listElems = addCloseToMenu(listElems, "Close menu", newDiv);
	}
	else {
		// Prepare the data
		let data_to_send = [];

		data_to_send[0] = xsdString;
		data_to_send[1] = ontoString;

		console.log(xsdString + ", " + ontoString);

		// Send the data

		xmlhttp = new XMLHttpRequest();
		var url = "/is_valid/";
		xmlhttp.open("POST", url, true);
		xmlhttp.setRequestHeader("Content-type", "application/json");
		xmlhttp.onreadystatechange = function () { //Call a function when the state changes.
			var a;
			if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {

				responseText = xmlhttp.responseText;

				console.log(responseText);

				if (responseText == "True") {
					listElems = addItemToMenu(listElems, "Add to association", newDiv, addToAssociation.bind(ev, currentString, startingType));

					listElems = addItemToMenu(listElems, "Remove association", newDiv, removeAssociation.bind(ev, currentString, startingType));

					listElems = addCloseToMenu(listElems, "Close menu", newDiv);

				}
				else {


					listElems = addCloseToMenu(listElems, "Close menu", newDiv);
				}

			}
		}
		// You should set responseType as blob for binary responses
		var data = {
			"pair": data_to_send
		};

		xmlhttp.send(JSON.stringify(data));

	}

	newDiv.appendChild(listElems);
	document.body.appendChild(newDiv);
}

function addToAssociation(startingString, startingType) {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let rows = doc.querySelectorAll("table tr");

	var startingColumn = undefined;

	if (startingType == "XSD") {
		startingColumn = 0;
	}
	else if (startingType == "Ontology") {
		startingColumn = 1;
	}

	let otherColumn = Math.abs(startingColumn - 1);
	let alreadyInserted = false;

	for (let i = 1; i < rows.length; ++i) {
		console.log(i);
		let startingSelector = rows[i].childNodes[startingColumn].firstChild;

		let startingValue = undefined;
		if (startingSelector.innerHTML.startsWith("<select>")) {
			startingValue = startingSelector.options[startingSelector.selectedIndex].text;
		}
		else {
			startingValue = startingSelector.firstChild.innerHTML;
		}
		if (startingValue === startingString) {
			alert("The value has already been inserted");
			alreadyInserted = true;
		}
	}

	if (alreadyInserted == false) {
		startingString = document.querySelectorAll(".right-menu span")[1].textContent;
		if (startingType == "XSD") {
			chooseStd(startingString, doc.querySelector(".selectedForAssociation"));
		}
		else if (startingType == "Ontology") {
			chooseOntology(startingString, doc.querySelector(".selectedForAssociation"));
		}
	}
}

function chooseStd(value, tr) {

	if (tr != null) {
		let stdSel = tr.childNodes[0].firstChild;
		stdSel.parentNode.innerHTML = "<span>" + value + "</span>";
		document.querySelector(".right-menu").style.backgroundColor = "rgba(0, 153, 51, 0.9)";
		let ontSel = tr.childNodes[1].firstChild;

		if (!ontSel.parentNode.innerHTML.startsWith("<span>")) {
			ontSel.parentNode.innerHTML = "<span><i>Select a node</i></span>";
		}
	}
	else {
		document.querySelector(".right-menu").style.backgroundColor = "rgba(174, 29, 63, 0.5)";
	}

}

function chooseOntology(value, tr) {
	if (tr != null) {
		let ontSel = tr.childNodes[1].firstChild;
		ontSel.parentNode.innerHTML = "<span>" + value + "</span>";
		document.querySelector(".right-menu").style.backgroundColor = "rgba(0, 153, 51, 0.9)";
		let stdSel = tr.childNodes[0].firstChild;

		if (!stdSel.parentNode.innerHTML.startsWith("<span>")) {
			stdSel.parentNode.innerHTML = "<span><i>Select a node</i></span>";
		}
	}
	else {
		document.querySelector(".right-menu").style.backgroundColor = "rgba(174, 29, 63, 0.5)";
	}
}

function dispatchAddAssociation(doc) {
	var evt = document.createEvent("HTMLEvents");
	evt.initEvent("click", false, true);
	doc.getElementById("addAssociation").dispatchEvent(evt);
}

function removeAssociation(startingString, startingType) {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let rows = doc.querySelectorAll("table tr");

	if (startingType == "XSD") {
		removeXSD(startingString, rows);
	}
	else if (startingType == "Ontology") {
		removeOntology(startingString, rows);
	}

	//alert("REMOVE " + startingString + ", " + startingType);
}

function removeXSD(string, rows) {
	for (let i = 1; i < rows.length; ++i) {
		if (getSelection(rows[i].childNodes[0].firstChild) == string) {
			// Copy other menu
			let otherMenuHTML = rows[i].childNodes[1].innerHTML;
			// Remove association
			rows[i].remove();
			// Add new line
			var obj = document.getElementById("associations-embed");
			var doc = obj.contentDocument; // get the inner DOM
			let addAssocButton = doc.getElementById("addAssociation");
			var evt = document.createEvent("HTMLEvents");
			evt.initEvent("click", false, true); // adding this created a magic and passes it as if keypressed
			addAssocButton.dispatchEvent(evt);
			// Get new line
			let allRows = doc.querySelectorAll("table tr");
			let lastRow = allRows[allRows.length - 1];
			// Get the ontology cell
			lastRow.childNodes[1].innerHTML = otherMenuHTML;
		}
	}
}


function removeOntology(string, rows) {
	for (let i = 1; i < rows.length; ++i) {
		if (getSelection(rows[i].childNodes[1].firstChild) == string) {
			// Copy other menu
			let otherMenuHTML = rows[i].childNodes[0].innerHTML;
			// Remove association
			rows[i].remove();
			// Add new line
			var obj = document.getElementById("associations-embed");
			var doc = obj.contentDocument; // get the inner DOM
			let addAssocButton = doc.getElementById("addAssociation");
			var evt = document.createEvent("HTMLEvents");
			evt.initEvent("click", false, true); // adding this created a magic and passes it as if keypressed
			addAssocButton.dispatchEvent(evt);
			// Get new line
			let allRows = doc.querySelectorAll("table tr");
			let lastRow = allRows[allRows.length - 1];
			// Get the ontology cell
			lastRow.childNodes[0].innerHTML = otherMenuHTML;
		}
	}
}


function findAssociation(currentString, startingType) {
	if (startingType == "XSD") {
		return findAssociationGivenXSD(currentString);
	}
	else if (startingType == "Ontology") {
		return findAssociationGivenOntology(currentString);
	}
}

function findAssociationGivenXSD(currentString) {
	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM
	let rows = doc.querySelectorAll("table tr");
	for (let i = 1; i < rows.length; ++i) {
		let xsdSelector = rows[i].childNodes[0].firstChild;
		let xsdValue = undefined;
		if (xsdSelector.innerHTML.startsWith("<select>")) {
			xsdValue = xsdSelector.options[xsdSelector.selectedIndex].text;
		}
		else {
			xsdValue = xsdSelector.firstChild.innerHTML;
		}

		if (xsdValue == currentString) {
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
	for (let i = 1; i < rows.length; ++i) {
		let ontoSelector = rows[i].childNodes[1].firstChild;

		let ontoValue = undefined;
		if (ontoSelector.innerHTML.startsWith("<select>")) {
			ontoValue = ontoSelector.options[ontoSelector.selectedIndex].text;
		}
		else {
			ontoValue = ontoSelector.firstChild.innerHTML;
		}

		// let ontoValue = ontoSelector.options[ontoSelector.selectedIndex].text;
		if (ontoValue == currentString) {
			let xsdSelector = rows[i].childNodes[0].firstChild;
			let xsdValue = xsdSelector.options[xsdSelector.selectedIndex].text;
			return xsdValue;
		}
	}
	return "-";
}

function xsdRC(ev) {
	let currentString = this.innerHTML;


	if (currentString.startsWith("<span")) {
		currentString = currentString.replace(/<span class=\"hiddenText\">name=<\/span>/gi, "");
		currentString = currentString.replace(/<span class=\"hiddenText\">\"<\/span>/gi, "");
	}

	if (currentString.startsWith("name")) {
		currentString = currentString.replace(/name="/gi, "").replace(/"/gi, "");
	}


	createRMenu(ev, currentString, "XSD");
	ev.preventDefault();
}

function ontoRC(ev) {
	let currentString = this.querySelector("title").innerHTML;
	createRMenu(ev, currentString, "Ontology");
	ev.preventDefault();
}

function attachAssociationListener() {

	var obj = document.getElementById("associations-embed");
	var doc = obj.contentDocument; // get the inner DOM

	setTimeout(function () {
		if (doc != null && doc != undefined) {
			var el = doc.getElementById("locateAssociation"); // assuming the embedded document has such an element
			if (el == null) {
				attachAssociationListener();
			}
			else {
				el.addEventListener("click", showAssociationOnGraph, false);
			}
		} else {
			attachAssociationListener();
		}

	}, 500);
}

function getSelection(cell) {
	if (cell.innerHTML.startsWith("<option>") || cell.innerHTML.startsWith("<optgroup")) {
		return cell.options[cell.selectedIndex].text;
	}
	else if (cell.innerHTML.startsWith("<span")) {
		return cell.firstChild.innerHTML;
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

	let valid = true;


	let stdValues = [];
	let ontValues = [];

	// Consider the data cell by cell
	for (let i = 1; i < stdCells.length; ++i) {
		let stdCell = stdCells[i].childNodes[0].firstChild;
		let stdCellValue = getSelection(stdCell);

		if (stdValues.includes(stdCellValue) || stdCellValue == "-") {
			stdCell.parentNode.className = "invalidRow";
			valid = false;
		}
		else {
			stdCell.parentNode.className = "validRow";
		}
		stdValues.push(stdCellValue);
	}

	for (let i = 1; i < ontCells.length; ++i) {
		let ontCell = ontCells[i].childNodes[1].firstChild;
		let ontCellValue = getSelection(ontCell);

		if (ontValues.includes(ontCellValue) || ontCellValue == "-") {
			ontCell.parentNode.className = "invalidRow";
			valid = false;
		}
		else {
			ontCell.parentNode.className = "validRow";
		}
		ontValues.push(ontCellValue);
	}



	if (valid) {

		// Prepare the data
		let data_to_send = {};
		let data_length = stdValues.length;

		for (let i = 0; i < data_length; ++i) {
			data_to_send[stdValues[i]] = ontValues[i];
		}

		// Send the data

		xmlhttp = new XMLHttpRequest();
		var url = "/download/";
		xmlhttp.open("POST", url, true);
		xmlhttp.setRequestHeader("Content-type", "application/json");
		xmlhttp.onreadystatechange = function () { //Call a function when the state changes.
			var a;
			if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
				var filename = "output.zip";
				var disposition = xmlhttp.getResponseHeader('Content-Disposition');
				if (disposition && disposition.indexOf('attachment') !== -1) {
					var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
					var matches = filenameRegex.exec(disposition);
					if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
				}
				// Trick for making downloadable link
				a = document.createElement('a');
				a.href = window.URL.createObjectURL(xmlhttp.response);
				// Give filename you wish to download
				a.download = filename;
				a.style.display = 'none';
				document.body.appendChild(a);
				a.click();
			}

		}

		// You should set responseType as blob for binary responses
		xmlhttp.responseType = 'blob';
		var data = {
			"associations": data_to_send
		};

		console.log(data);
		xmlhttp.send(JSON.stringify(data));
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
	if (degreeCollapsing != "0") {
		var resetButton = docOnt.getElementById("reset-button");
		var clickReset = document.createEvent("HTMLEvents");
		clickReset.initEvent("click", false, true);
		resetButton.dispatchEvent(clickReset);
	}

	var searchBoxOnt = docOnt.getElementById("search-input-text");
	searchBoxOnt.value = destination;


	var pauseMovement = docOnt.getElementById("pause-button");
	if (pauseMovement.className != "paused highlighted") {
		setTimeout(function () {
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
