<?php

?>

<!-- HTML code to display data in tabular format -->
<!DOCTYPE html>
<html lang="en">
<!-- HTML code to display data in tabular format -->

<head>
  <meta charset="UTF-8">
  <title>Delete Contact</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
  <!-- CSS FOR STYLING THE PAGE  -->
  <link rel="stylesheet" type="text/css" href="css/style.css" />
  <!-- <script type="text/javascrpt" src=js/vehicles.js></script> -->

<body>
<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <!-- class="logo_colour", allows you to change the colour of the text -->
        <h1><a href="index.php">SnoDEM<span class="logo_colour">_MITRU</span></a></h1>
        <h2>Delete Vehicle</h2>
      </div>
    <div id="menubar">
			<ul id="menu">
			 <li><a href="index.php">Home</a></li>
            <li><a href="vehicles.php">Vehicles</a></li>
            <li class="selected"><a href="add_vehicle.php">New Vehicles</a></li>
            <li><a href="vehicle_types.php">Vehicle Types</a></li>
            <li><a href="base_loc.php">Base Locations</a></li>
         </ul>

      </div>
   </div>
   <div id="site_content">
     <div id="content">
        <!-- add content here -->
        <?php
            $parameter = $_SERVER['QUERY_STRING'];
            echo '<h2> Delete Not Implemented </h2>';
    			echo "<p>" . $parameter . "</p>";
			?>  
     </div>
   </div>
   <div id="footer">
      <p><a href="index.html">Home</a> | <a href="vehicles.php">Vehicles</a> | <a href="alertsandalarms.php">Alerts and Alarms</a>
      | <a href="rules.php">Rules</a>
      | <a href="contacts.php">Alert/Alarm Contacts</a> | <a href="contact.html">Contact Us</a></p>
      <p>Copyright &copy; Snohomish County Department of Emergency Management </p>
   </div>
 </div>
</body>
</html>