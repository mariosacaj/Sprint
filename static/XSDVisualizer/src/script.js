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
          if (tspans[i].innerHTML.includes(">" + term + "<")) {
              break;
          }
          if (tspans[i].innerHTML.includes('"' + term + '"<')) {
              break;
          }
      }
    }

    let position = found.parentNode.parentNode.getAttribute("transform").split("translate(")[1].split(")")[0];

    let posX = position.split(",")[0];
    let posY = position.split(",")[1];

    panZoom.zoom(3);
    panZoom.pan({x: 0, y: 0});
    var realZoom = panZoom.getSizes().realZoom;

    panZoom.pan
    ({
        //x: (panZoom.getSizes().width / 2) - (posX * realZoom),
        //y: (panZoom.getSizes().height / 2) - (posY * realZoom)
        x: -posX,
        y: -posY
    });

	found.parentNode.parentNode.getElementsByTagName("circle")[0].style.stroke = "#00bfff";
	found.parentNode.parentNode.getElementsByTagName("circle")[0].style.fill = "#00bfff";
	found.parentNode.parentNode.getElementsByTagName("text")[0].style.fill = "blue";
}
