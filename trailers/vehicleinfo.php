<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fetch API Demo</title>
    <link rel="stylesheet" href="css/style.css">
	<script>
	function showVehicle(str) {
	  if (str == "") {
		document.getElementById("txtHint").innerHTML = "";
		return;
	  } else {
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
		  if (this.readyState == 4 && this.status == 200) {
			document.getElementById("txtHint").innerHTML = this.responseText;
		  }
		};
		xmlhttp.open("GET","src/vehicledata.php?vehicle="+str,true);
		xmlhttp.send();
	  }
	}
	</script>
</head>
<body>
	<h1> Vehicle Inforformation for past 72 hours </h1>
	<form>
		<select name="vehicle" onchange="showVehicle(this.value)">
		<option value="">Select a vehicle:</option>
		<option value="1">White</option>
		<option value="2">Grey</option>
		<option value="3">Black</option>
		</select>
	</form>
	<br>
	<div id="txtHint"><b>Vehicle info will be listed here.</b></div>

</body>
</html>
