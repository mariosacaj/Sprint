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

function createMenu() {
	let table = document.querySelector("table");
	
	let selectMenuStandard = document.createElement("select");
	let emptyOption = document.createElement("option");
	emptyOption.innerHTML = "-";
	selectMenuStandard.appendChild(emptyOption);
	for(let i=0; i<arraysElements[0].length; ++i) {
		let option = document.createElement("option");
		option.innerHTML = getAfterColon(arraysElements[0][i]);
		selectMenuStandard.append(option);
	}

	let selectMenuOntology = document.createElement("select");
	emptyOption = document.createElement("option");
	emptyOption.innerHTML = "-";
	selectMenuOntology.append(emptyOption);
	for(let i=0; i<arraysElements[1].length; ++i) {
		let option = document.createElement("option");
		option.innerHTML = getAfterColon(arraysElements[1][i]);
		selectMenuOntology.append(option);
	}

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
	let selectedOntology = this.innerHTML;
	let otherMenu = this.parentNode.parentNode.querySelector("td select");
	let suggStd = suggestedStandards(this.value);
	fillMenu(otherMenu, suggStd);
}

function filterOntology() {
	let selectedStandard = this.innerHTML;
	let otherMenu = this.parentNode.parentNode.querySelectorAll("td select")[1];
	let suggOnt = suggestedOntologies(this.value);
	fillMenu(otherMenu, suggOnt);
}

function fillMenu(menu, array) {
	menu.innerHTML = "";
	for(let i=0; i<array.length; ++i) {
		let suggestion = document.createElement("option");
		suggestion.innerHTML = array[i];
		menu.appendChild(suggestion);
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
