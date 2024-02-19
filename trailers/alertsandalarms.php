<?php


function getColVal($row, $column)
{
        $rtn = $row[$column];
        if ($column == 'vehicles')
        {
                $rtn = vehicle_list($rtn);
        }
        return $rtn;
}

require_once('dbconfig.php');

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
  <script type="text/javascrpt" src=js/alarms.js></script>

</head>

<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <!-- class="logo_colour", allows you to change the colour of the text -->
        <h1><a href="index.php">SnoDEM<span class="logo_colour">_MITRU</span></a></h1>
        <h2>Alerts and Alarms</h2>
      </div>

      <div id="menubar">
        <ul id="menu">
          <!-- put class="selected" in the li tag for the selected page - to highlight which page you're on -->
          <li><a href="index.php">Home</a></li>
          <li><a href="vehicles.php">Vehicles</a></li>
          <li class="selected"><a href="alertsandalarms.php">Alerts and Alarms</a></li>
          <li><a href="rules.php">Rules</a></li>
          <li><a href="contacts.php">Alert/Alarm Contacts</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
     </div>
   </div>
    <div id="site_content">
      <div id="content">
        <!-- TABLE CONSTRUCTION -->
        <!-- PHP CODE TO FETCH COLUMN NAMES -->
        <?php			
            
           // SQL query to select data from database
           //$sql = "SELECT * FROM contacts ORDER BY id";
           // 	a.cleared, a.clear_time, a.cleared_sent,
           $sql_where = " WHERE a.cleared = 0 ";

           if (isset($_GET['vehicle']) && !empty($_GET['vehicle'])) {
               $sql_where  = ' WHERE a.cleared = 0 AND a.v_id=' . $_GET['vehicle'] ;
           } 

           $sql_order = " ORDER BY a.v_id ASC, a.severity ASC, a.post_time DESC;";

            $sql = "SELECT a.id, a.rule_id, c.rule_name, a.post_time, a.sent, a.sent_time,
                   a.acknowledged, a.acknowledge_time,
                   a.v_id, b.name as vehicle, a.count, a.severity, a.message
                   FROM status_queue a
                   INNER JOIN vehicles b
                   ON a.v_id = b.id
                   INNER JOIN rules c
                   ON a.rule_id = c.id " . $sql_where . $sql_order; 
           $rs = $conn->query($sql);
           $conn->close();
				
        ?>
        <table>
            <tr>
               <?php
                   for ( $i = 0; $i < $rs->columnCount(); $i++)
                   {
                      $col = $rs->getColumnMeta($i);
                      $columns[] = $col['name'];
                      echo "<th>" . $col['name'] . "</th>";    
                   }
                       
               ?>
            </tr>
            <!-- PHP CODE TO FETCH DATA FROM ROWS -->
            <?php
                $rownumber = 0;
                // LOOP TILL END OF DATA
                while($rows=$rs->fetch())
                {
                //$bname = 'button'.$rows['v_id']
            ?>
            <tr>
                <!-- FETCHING DATA FROM EACH
                    ROW OF EVERY COLUMN -->
                        <?php
                           for ( $i = 0; $i < count($columns); $i++)
                           {
                                echo "<td>" . getColVal($rows,$columns[$i]) . "</td>";
                            }
                            //echo "<td><input type='checkbox' name='checkbox[" . $rownumber . "]' value='". $rows['id'] . "'</td>";

                                ?>

            </tr>
            <?php
                    $rownumber = $rownumber + 1;
                }
            ?>
        </table>
        <?php   $conn=null; ?>
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


