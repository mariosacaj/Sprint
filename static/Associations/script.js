document.addEventListener("DOMContentLoaded", getAssociations, false);
var arraysElements  = [];
var JSONtext = undefined;

function getAssociations() {

	var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
	JSONtext = xhttp.responseText;
	arraysElements = getTerms(JSONtext);
	createMenu();
document.getElementById("addAssociation").addEventListener("click", createMenu, false);
    }
};
xhttp.open("GET", "http://127.0.0.1:8000/getAssociations", true);
xhttp.send();
}

function getTerms(JSONtext) {
	var obj = JSON.parse(JSONtext); // parsed JSON
	let first = [];
	let second = [];
	for(let key in obj) {
		first.push(key);
		for(let i=0; i<obj[key].length; ++i) {
			second.push(obj[key][i][0]);
		}
	}
	return [first, second];
}

function getAfterColon(string) {
	if(string.includes(":")) {
		splitted_string = string.split(":");
		return splitted_string[splitted_string.length - 1];
	}
	return string;
}

function createMenuStandard(table) {

	
	let selectMenuStandard = document.createElement("select");
	let emptyOption = document.createElement("option");
	emptyOption.innerHTML = "-";
	selectMenuStandard.appendChild(emptyOption);
	for(let i=0; i<arraysElements[0].length; ++i) {
		let option = document.createElement("option");
		option.innerHTML = getAfterColon(arraysElements[0][i]);
		selectMenuStandard.append(option);
	}
	return selectMenuStandard;
}

function createMenuOntology(table) {
	let selectMenuOntology = document.createElement("select");
	emptyOption = document.createElement("option");
	emptyOption.innerHTML = "-";
	selectMenuOntology.append(emptyOption);
	for(let i=0; i<arraysElements[1].length; ++i) {
		let option = document.createElement("option");
		option.innerHTML = getAfterColon(arraysElements[1][i]);
		selectMenuOntology.append(option);
	}
	return selectMenuOntology;
}

function cleanEmpty() {
	let allRows = document.querySelectorAll("table tr");
	for(let i=1; i<allRows.length; ++i) {
		let firstColumnValue = allRows[i].childNodes[0].firstChild.value;
		if(firstColumnValue != undefined) {
			firstColumnValue = firstColumnValue.innerHTML;
		}
		else {
			firstColumnValue = "-";
		}
		
		let secondColumnValue = allRows[i].childNodes[1].firstChild.value;
		if(secondColumnValue != undefined) {
			secondColumnValue = secondColumnValue.innerHTML;
		}
		else {
			secondColumnValue = "-";
		}

		if(firstColumnValue == "-" && secondColumnValue == "-") {
			allRows[i].remove();
		}	
	}
}

function createMenu() {
	
	//cleanEmpty();
	let table = document.querySelector("table");

	let selectMenuStandard = createMenuStandard(table);
	let selectMenuOntology = createMenuOntology(table);
	

	let newTR = document.createElement("tr");
	let newTDStand = document.createElement("td");
	let newTDOnto = document.createElement("td");
	let tdLocate = document.createElement("td");
	newTDStand.appendChild(selectMenuStandard);
	newTDOnto.appendChild(selectMenuOntology);
	let locateText = document.createElement("span");
	locateText.innerHTML = "Locate";
	locateText.addEventListener("click", colorLine, false);
	tdLocate.appendChild(locateText);
	newTR.appendChild(newTDStand);
	newTR.appendChild(newTDOnto);
	newTR.appendChild(tdLocate);
	table.appendChild(newTR);

	selectMenuOntology.addEventListener("change", filterStandard, false);
	selectMenuStandard.addEventListener("change", filterOntology, false);
}

function colorLine() {

	let table = document.getElementsByTagName("table")[0];
	let numRows = table.rows.length;
	for(let i=0; i<numRows; ++i) {
		document.querySelectorAll("table tr")[i].className = "";
		if(document.querySelectorAll("table tr")[i].style.backgroundColor == "black") {
		document.querySelectorAll("table tr")[i].style.backgroundColor = "rgb(200, 200, 200)";
	}
	}
	this.parentNode.parentNode.style.backgroundColor = "black";
	this.parentNode.parentNode.style.color = "white";
	this.parentNode.parentNode.className = "selectedRow";

	var evt = document.createEvent("HTMLEvents"); 
        evt.initEvent("click", false, true); // adding this created a magic and passes it as if keypressed
        document.getElementById("locateAssociation").dispatchEvent(evt);
}

function suggestedStandards(ontologyValue) {
	var obj = JSON.parse(JSONtext); // parsed JSON
	let suggestions = [];
	for(let key in obj) {
		for(let i=0; i<obj[key].length; ++i) {
			if(obj[key][i][0].includes(ontologyValue)) {
				suggestions.push(key);
				break;
			}
		}
	}
	return suggestions;
}

function suggestedOntologies(standardValue) {
	var obj = JSON.parse(JSONtext); // parsed JSON
	let suggestions = [];
	for(let key in obj) {
		if(key.includes(standardValue)) {
			for(let i=0; i<obj[key].length; ++i) {
				suggestions.push(getAfterColon(obj[key][i][0]));
			}
	}
		
	}
	return suggestions;
}

function filterStandard() {
	//let selectedOntology = this.innerHTML;
	let td = this.parentNode.parentNode.querySelector("td");
	let otherMenu = td.firstChild;

	if(td.innerHTML.startsWith("<select>")) {
		let currentStd = otherMenu.options[otherMenu.selectedIndex].text;	
		let suggStd = suggestedStandards(this.value);

		fillMenu(otherMenu, suggStd, currentStd);
	}
	
}

function filterOntology() {
	//let selectedStandard = this.innerHTML;
	let td = this.parentNode.parentNode.querySelectorAll("td")[1];
	let otherMenu = td.firstChild;

	if(td.innerHTML.startsWith("<select>")) {
		let currentOntology = otherMenu.options[otherMenu.selectedIndex].text;
		let suggOnt = suggestedOntologies(this.value);
		fillMenu(otherMenu, suggOnt, currentOntology);
	}
}

function fillMenu(menu, array, currentValue) {
// devo prendere current value altro emnu
	menu.innerHTML = "";
	let oldOption = document.createElement("option");
	console.log(array);
	console.log(currentValue);
	if(array.includes(currentValue)) {
		oldOption.innerHTML = currentValue;
	}
	else {
		oldOption.innerHTML = "-";
	}
	menu.append(oldOption);

	for(let i=0; i<array.length; ++i) {
		if(array[i] != currentValue) {
			let suggestion = document.createElement("option");
			suggestion.innerHTML = array[i];
			menu.appendChild(suggestion);
		}
	}
}

function showData(text) {
	let allTerms = getTerms(text);
	createMenu(allTerms);

	first = allTerms[0];
	second = allTerms[1];
	secondRed = [];

	for(let term in second) {
		secondRed.push(getAfterColon(term));
	}
	

	let unlist = document.getElementsByTagName("ul")[0];
	let assocArray = text.split("\n");
	for(let i=0; i<assocArray.length; ++i) {
		let completeString = assocArray[i];
		newAssoc = document.createElement("li");
		span1 = document.createElement("span");
		span2 = document.createElement("span");
		span1.className = "source";
		span2.className = "destination";
		let source = completeString.split("], [")[0].split("[")[1].replace(/'/gi,"").replace(/,/gi,"").replace(/ /gi,"");
		let destination = completeString.split("], [")[1].split("]")[0].replace(/'/gi,"").replace(/,/gi,"").replace(/ /gi,"");;
		let sourceText = document.createTextNode(source);
		let destinationText = document.createTextNode(destination);
		span1.appendChild(sourceText);
		span2.appendChild(destinationText);
		newAssoc.appendChild(span1);
		newAssoc.appendChild(span2);
		unlist.appendChild(newAssoc);
		newAssoc.addEventListener("click", clickOnAssociation, false);

	}
}

function clickOnAssociation() {
	if(this.style.backgroundColor == "black") {
		this.style.backgroundColor = "white";
		this.style.color = "black";
	}
	else {
		this.style.backgroundColor = "black";
		this.style.color = "white";
	}
}
