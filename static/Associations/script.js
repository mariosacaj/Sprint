document.addEventListener("DOMContentLoaded", getAssociations, false);

function getAssociations() {

	var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       showData(xhttp.responseText);
    }
};
xhttp.open("GET", "http://127.0.0.1:8000/getAssociations", true);
xhttp.send();
}

function showData(text) {
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
