<?php
require_once('config.php');

$mysqli = new mysqli(DB_SERVER, DB_USERNAME,
                DB_PASSWORD, DB_NAME);

// Checking for connections
if ($mysqli->connect_error) {
    echo '<script type="text/javascript"> 
            alert(" DB Connection failed");
         </script>';
}

//$sql=" SELECT id, v_id, enabled, rule_name, rule_class, rule_function FROM rules;";
$sql="SELECT r.id, v.name as vehicle, r.rule_name, r.rule_class, r.rule_function FROM rules r
      INNER JOIN vehicles v
      ON v.id = r.v_id
      ;";

$result = $mysqli->query($sql);
$mysqli->close();
?>

<!-- HTML code to display data in tabular format -->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>MITRU Information</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
  <!-- CSS FOR STYLING THE PAGE  -->
  <link rel="stylesheet" type="text/css" href="css/style.css" />
  <script type="text/javascript">
  // rule update functions

  function edit_rule(elem){
    var data= elem.name;
    //console.log(data);
    //alert('This alert box was called with the id click event =' + data);
    location.href = "edit_rule.php?rule=" + data;   
  }

  function add_rule(){
    //console.log(data);
    //alert('This alert box was called with the add click event');
    location.href = "add_rule.php";
  }

  function delete_rule(elem) {

  }
  </script>

</head>

<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <!-- class="logo_colour", allows you to change the colour of the text -->
        <h1><a href="index.php">SnoDEM<span class="logo_colour">_MITRU</span></a></h1>
        <h2>Rules</h2>
      </div>

      <div id="menubar">
        <ul id="menu">
          <!-- put class="selected" in the li tag for the selected page - to highlight which page you're on -->
          <li><a href="index.php">Home</a></li>
          <li><a href="vehicles.php">Vehicles</a></li>
          <li><a href="alertsandalarms.php">Alerts and Alarms</a></li>
          <li class="selected"><a href="rules.php">Rules</a></li>
          <li><a href="contacts.php">Alert/Alarm Contacts</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
     </div>
   </div>
   <div id="site_content">
     <div id="content">
     <!-- insert content here -->
        <table>
            <tr>
                <th>    </th>
                <!-- <th>enabled</th> -->
                <<th>rule_name</th>
                <th>vehicle</th>
                <th>rule_class</th>
                <th>rule_function</th>
                <!-- <th>Status</th> -->
            </tr>
            <!-- PHP CODE TO FETCH DATA FROM ROWS -->
            <?php

                // LOOP TILL END OF DATA
                
                while($rows=$result->fetch_assoc())
                {
                $bname =  $rows['id'];
                //$vname = $rows['rule_name'];
                $vname = "Edit";
            ?>       
                <td><input  onclick='edit_rule(this)' type="button" width="fit-content" 
                    value=<?php echo $vname;?> name=<?php echo $bname;?> />
                    </td> 
                <td><?php echo $rows['rule_name'];?></td>  
                <td><?php echo $rows['vehicle'];?></td>
                <!-- <td><?php echo $rows['enabled'];?></td> -->
                
                <td><?php echo $rows['rule_class'];?></td>
                <td><?php echo $rows['rule_function'];?></td>
               
            </tr>
            <?php
                }
            ?>                 
				<tr>
				<td>           
				   <input type="button" name="add" value="add" onclick= "add_rule()" > 
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
  <div>
</body>
</html>
