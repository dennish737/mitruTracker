<?php

// Process delete operation after confirmation
if(isset($_POST["id"]) && !empty($_POST["id"])){
    // Include config file
    require_once "dbconfig.php";
    
    // Prepare a delete statement
    $sql = "DELETE FROM employees WHERE id = ?";
    
    if($stmt = mysqli_prepare($link, $sql)){
        // Bind variables to the prepared statement as parameters
        mysqli_stmt_bind_param($stmt, "i", $param_id);
        
        // Set parameters
        $param_id = trim($_POST["id"]);
        
        // Attempt to execute the prepared statement
        /*
        if(mysqli_stmt_execute($stmt)){
            // Records deleted successfully. Redirect to landing page
            header("location: contacts.php");
            exit();
        } else{
            echo "Oops! Something went wrong. Please try again later.";
        }
        */
        header("location: contacts.php");
    }
     
    // Close statement
    mysqli_stmt_close($stmt);
    
    // Close connection
    //$conn_close($link);
} else{
    // Check existence of id parameter
    if(empty(trim($_GET["id"]))){
        // URL doesn't contain id parameter. Redirect to error page
        //header("location: contacts.php");
        exit();
    }
}
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
   <?php
     require_once "dbconfig.php";
     $name = "me";
     if(!empty(trim($_GET["id"]))){
     	  $contact_id = trim($_GET["id"]);
        $sql = "SELECT name FROM contacts  WHERE id=$contact_id LIMIT=1; ";
        //$result = $conn->query($sql);
        $name = $sql;

     }       

  ?>
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
          <li><a href="alertsandalarms.php">Alerts and Alarms</a></li>
          <li><a href="rules.php">Rules</a></li>
	       <li><a href="contacts.php">Alert and Alarm Contacts</a></li>
          <li> <a href="contact.html">Contact Us</a></li>
         </ul>

      </div>
   </div>
   <div id="site_content">
     <div id="content">
        <!-- add content here -->
        <h2 class="mt-5 mb-3">Delete Record</h2>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                        
              <input type="hidden" name="id" value="<?php echo trim($_GET["id"])?>"/>
              <p>Are you sure you want to delete this contact record (<?php echo trim($_GET["id"])  . "-" . $name ; ?> )</p>
              <p>
              <input type="submit" value="Yes" class="btn btn-danger">
              <a href="contacts.php" class="btn btn-secondary">No</a>
              </p>
       </form>
      <?php
          // Close connection
          $conn_close($link);
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