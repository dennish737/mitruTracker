<!DOCTYPE html>
<html>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<script>
function getVehicleName(str) {

        var v_name = "";
        if (str == "1") {
                v_name = "White" ;
        } else if (str == "2") {
                v_name = "Grey";
        } else if (str == "3") {
                v_name = "Black";
        } else {
                v_name = "Unknown";
        }
        return v_name;
};

var vehicle = "0";

const queryString = window.location.search;

const urlParams = new URLSearchParams(queryString);

if (urlParams.has('vehicle')) {
        vehicle = urlParams.get('vehicle');
} else {
        vehicle = "1";
}

let vehicleName = getVehicleName(vehicle);
</script>

<body>

<script>
var hdr = '<h1> ' + vehicleName + ' Temperature for past 72 hours </h1>';
document.write(hdr);
</script>


<div id="myPlot" style="width:100%;max-width:700px"></div>

<div id="myPlot" style="width:100%;max-width:700px"></div>

<h3> Plot Data </h3>
<p id="demo"></p>

<script>

var xValues = [];
var yValues = [];

var xmlhttp = new XMLHttpRequest();

xmlhttp.onload = function() {
  myObj = JSON.parse(this.responseText);
  let text = ""
  for (let x in myObj) {
    xValues.push( myObj[x].t_diff);
    yValues.push(myObj[x].temp);
  }
  for(let x in xValues) {
    text += xValues[x] + ", " + yValues[x] + "<br>";
  }
  document.getElementById("demo").innerHTML = text;

  var data = [{
        x: xValues,
        y: yValues,
        //mode: "markers",
        //type: "scatter"
        mode: "line"
  }];

  var layout = {
    xaxis: {range: [0, 4320], title: "Time in minutes"},
    yaxis: {range: [30, 115], title: "Temperature \u00B0F"},
    title: "Vehicle Temperature for last 72 hours"
        };


  // Display using Plotly
  Plotly.newPlot("myPlot", data, layout);

};
xmlhttp.open("GET", "src/volt_temp_data.php?vehicle=" + vehicle, true);
xmlhttp.send();

</script>

<p>End of Test</p>

</body>
</html>


