function addEL() {
	document.getElementById("searchTerm").addEventListener("change", searchTerm, false);
}

function searchTerm() {
	let term = this.value;
	
	var tspans = document.getElementsByTagName("tspan");
	var found;

	for (var i = 0; i < tspans.length; i++) {
	  if (tspans[i].innerHTML.includes(term)) {
	    found = tspans[i];
	    break;
	  }
	}

	let position = found.parentNode.parentNode.getAttribute("transform").split("translate(")[1].split(")")[0];

	let posX = position.split(",")[0];
	let posY = position.split(",")[1];

	panZoom.zoom(2);
	panZoom.pan({x:0,y:0});
	var realZoom= panZoom.getSizes().realZoom;

	panZoom.pan
	({  
	x: -(posX*realZoom)+(panZoom.getSizes().width/2),
	y: -(posY*realZoom)+(panZoom.getSizes().height/2)
	});

	found.parentNode.parentNode.getElementsByTagName("circle")[0].style.stroke = "#00bfff";
	found.parentNode.parentNode.getElementsByTagName("circle")[0].style.fill = "#00bfff";
	found.parentNode.parentNode.getElementsByTagName("text")[0].style.fill = "blue";
}
