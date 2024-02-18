<?php
// Include configuration file
require_once "dbconfig.php";


?>

<!DOCTYPE html>
<html lang="en">
<!-- HTML code to display data in tabular format -->

<head>
  <meta charset="UTF-8">
  <title>MITRU Vehicles</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
  <!-- CSS FOR STYLING THE PAGE  -->
  <link rel="stylesheet" type="text/css" href="css/style.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <!-- <script type="text/javascript" src="js/vehicles.js"></script> -->
  <script type="text/javascript">
   // vehicle update scripts
  function edit_vehicle(elem){
    var data= elem.name;
    //console.log(data);
    //alert('This alert box was called with the id click event =' + data);
    location.href = "edit_vehicle.php?vehicle=" + data;   
  }

  function add_vehicle(){
    // location.href = "add_vehicle.php";
    //console.log(data);
    //alert('This alert box was called with the add click event');
    location.href = "add_vehicle.php";
  }

  function delete_delete (elem) {

  }
  </script>
  <script>
     $(document).ready(function(){
          $('[data-toggle="tooltip"]').tooltip();
        });
  </script>

</head>

<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <!-- class="logo_colour", allows you to change the colour of the text -->
        <h1><a href="index.php">SnoDEM<span class="logo_colour">_MITRU</span></a></h1>
        <h2>Vehicles</h2>
      </div>

      <div id="menubar">
        <ul id="menu">
          <!-- put class="selected" in the li tag for the selected page - to highlight which page you're on -->
          <li><a href="index.php">Home</a></li>
          <li class="selected"><a href="vehicles.php">Vehicles</a></li>
          <li><a href="alertsandalarms.php">Alerts and Alarms</a></li>
          <li><a href="rules.php">Rules</a></li>
          <li><a href="contacts.php">Alert/Alarm Contacts</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
     </div>
   </div>
    <div id="site_content">
      <div id="content">
        <!-- query table -->
        <?php
				// set the sql suffix
				$suffix = '';

				if (isset($_GET['vehicle']) && !empty($_GET['vehicle'])) {
					$suffix = ' WHERE id =' . $_GET['vehicle'] ;
				} else {
					$suffix = '';
				}


				// SQL query to select data from database
				$sql = "SELECT id, name, vid, status, base, 
					ST_Y(base_loc) as latitude, ST_X(base_loc) as longitude,
					CASE WHEN info_enabled = TRUE THEN 'ON' ELSE 'Off' END AS info_enable,
					CASE WHEN alert_enabled = TRUE THEN 'ON' ELSE 'Off' END AS alert_enable,
					CASE WHEN alarm_enabled = TRUE THEN 'ON' ELSE 'Off' END AS alarm_enable	
					FROM vehicles" . $suffix . ';' ;


             $result = $conn->query($sql);
             $conn->close();        
        ?>
        <!-- TABLE CONSTRUCTION -->
        <table>
            <tr>
            <th>Name</th>
            <th>APRS Name</th>
				<th>Status</th>
            <th>Base</th>
            <th>Base Latitude</th>
				<th>Base Longitude</th>
				<th>Info Messages</th>
				<th>Alert Messages</th>
				<th>Alarm Messages</th>	
				<th>    </th>			
            </tr>
            <!-- PHP CODE TO FETCH DATA FROM ROWS -->
			   <?php

                // LOOP TILL END OF DATA
                while($rows=$result->fetch_assoc())
                {
                	 $bname =  $rows['id'];
                   $vname = "Edit";
            ?>
            <tr>
                <!-- FETCHING DATA FROM EACH
                    ROW OF EVERY COLUMN -->
            <!-- <?php echo $rows['id'];?></td> -->

            <td><?php echo $rows['name'];?></td>
				<td><?php echo $rows['vid'];?></td>
            <td><?php echo $rows['status'];?></td>
            <td><?php echo $rows['base'];?></td>
            <td><?php echo $rows['latitude'];?></td>
				<td><?php echo $rows['longitude'];?></td>
            <td><?php echo $rows['info_enable'];?></td>
            <td><?php echo $rows['alert_enable'];?></td>
            <td><?php echo $rows['alarm_enable'];?></td>
            
            <td>                 
                <a href="vehicle_charts.html?vehicle=<?php echo $rows['id']; ?> " class="mr-3" title="View Data" data-toggle="tooltip">
                   <span class="fa fa-eye"></span>
                </a>
                <a href="vehicle_charts.html?vehicle=<?php echo $rows['id']; ?> " class="mr-3" title="View Alerts/Alarms" data-toggle="tooltip">
                   <span class="fa fa-eye"></span>
                </a>
                <a href="edit_vehicle.php?vehicle=<?php echo $rows['id']; ?> " class="mr-3" title="Update Record" data-toggle="tooltip">
                   <span class="fa fa-pencil"></span>
                </a>
                <a href="delete_vehicle.php?vehicle=<?php echo $rows['id']; ?>" title="Delete Record" data-toggle="tooltip">
                   <span class="fa fa-trash"></span>
                </a>
            </td>
            </tr>     
                  
            <?php
                }
            ?>
            
				<tr>
				<td>           
				   <input type="button" name="add" value="add" onclick= "add_vehicle()" > 
				</td>
				</tr>
				  
        </table>


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

