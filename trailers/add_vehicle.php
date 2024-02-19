<?php
require_once('dbconfig.php');

//define variables and initial values
$name = $vid = "";
$info_enabled = $alert_enabled = $alarm_enabled = 0;
$status = "";
$base = "";
$base_loc = "";

$name_err = $vid_err = $status_err = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){
    // Validate name
    $input_name = trim($_POST["name"]);
    if(empty($input_name)){
        $name_err = "Please enter a name.";
    } elseif(!filter_var($input_name, FILTER_VALIDATE_REGEXP, array("options"=>array("regexp"=>"/^[a-zA-Z\s]+$/")))){
        $name_err = "Please enter a valid name.";
    } else{
        $name = $input_name;
    }
    // [AKNWaknw][a-zA-Z]{0,2}[0123456789][a-zA-Z]{1,3}-[0123456789]{0,2}
    $input_vid = trim($_POST["vid"]);
    if(empty($input_vid)){
        $vid_err = "Please enter an APRS vehicle ID (Call sign + SSID).";
    } elseif(!filter_var($input_vid, FILTER_VALIDATE_REGEXP, array("options"=>array("regexp"=>"[AKNWaknw][a-zA-Z]{0,2}[0123456789][a-zA-Z]{1,3}-[0123456789]{0,2}")))){
        $vid_err = "Please enter a valid APRS vehicle ID (Call sign + SSID).";
    } else{
        $vid = $input_vid;
    }
    // Check input errors before inserting in database
    if(empty($name_err) && empty($vid_err) ){
        // Prepare an insert statement
        $sql = "INSERT INTO vehicles (name, vid, status, base, base_loc, info_enabled, alert_enabled, alarm_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        
        if($stmt = mysqli_prepare($mysqli, $sql)){
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "ssssssss", $param_name, $param_vid, $param_status, $param_base,
            			$param_base_loc, $param_info_enabled, $param_alert_inabled, $param_alarm_enabled);    
            
            //set parameters
            $param_name = $name;
            $param_vid = $vid;
            $param_status = $status;
            $param_base = $base;
            $param_base_loc = $base_loc;
            $param_info_enabled = $info_enabled;
            $param_alert_enabled = $alert_enabled;
            $param_alarm_enabled = $alarm_enabled;    
            // Attempt to execute the prepared statement
            if(mysqli_stmt_execute($stmt)){
                // Records created successfully. Redirect to landing page
                header("location: index.php");
                exit();
            } else{
                echo "Oops! Something went wrong. Please try again later.";
            }
        }
         
        // Close statement
        mysqli_stmt_close($stmt);
    }
    // Close connection
    mysqli_close($link);
}
?>

<!-- HTML code to display data in tabular format -->
<!DOCTYPE html>
<html lang="en">
<!-- HTML code to display data in tabular format -->

<head>
  <meta charset="UTF-8">
  <title>Add Vehicle</title>
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
        <h2>Add Vehicle</h2>
      </div>
    <div id="menubar">
			<ul id="menu">    
			 <li><a href="index.php">Home</a></li>
            <li><a href="vehicles.php">Vehicles</a></li>
            <li><a href="alertsandalarms.php">Alerts and Alarms</a></li>
            <li><a href="rules.php">Rules</a></li>
            <li><a href="contacts.php">Alert/Alarm Contacts</a></li>
            <li><a href="contact.html">Contact Us</a></li>
         </ul> 
              
      </div>
   </div>
   <div id="site_content">
     <div id="content">
          <h2 class="mt-5">Create Vehicle Record</h2>
          <p>Please fill this form and submit to add vehicle record to the database.</p>
          <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
               <div class="form-group">
                    <label>Name</label>
                    <input type="text" name="name" class="form-control <?php echo (!empty($name_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $name; ?>">
                    <span class="invalid-feedback"><?php echo $name_err;?></span>
               </div>
               <div class="form-group">
                   <label>Vehicle Id</label>
                   <textarea name="vid" class="form-control <?php echo (!empty($vid_err)) ? 'is-invalid' : ''; ?>"><?php echo $vid; ?></textarea>
                   <span class="invalid-feedback"><?php echo $address_err;?></span>
               </div>
               <div class="form-group">
                   <label>Satus</label>
                   <input type="text" name="status" class="form-control <?php echo (!empty($status_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $status; ?>">
                   <span class="invalid-feedback"><?php echo $salary_err;?></span>
                </div>
                <input type="submit" class="btn btn-primary" value="Submit">
               <a href="index.php" class="btn btn-secondary ml-2">Cancel</a>
          </form>
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