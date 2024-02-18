<?php
require_once "dbconfig.php";

function getColVal($row, $column)
{
        $rtn = $row[$column];
        if ($column == 'vehicles')
        {
                $rtn = vehicle_list($rtn);
        }
        return $rtn;
}

?>

?>
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>phpChart - Basic Chart</title>
</head>
<body>
<p> Hello </p> 
<?php
  echo "<p> file =" . dirname(dirname(__FILE__)) . "</p>";
  if (isset($_GET['vehicle']) && !empty($_GET['vehicle'])) {
  	
  	echo '<p> Get vehicle variable ( ' . $_GET['vehicle'] . '  ) value. </p>';
  } else {
   echo "<p> No vehicle value. </p>";
  }
?>
 
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
          //$sql = "my sql statement";
echo "<p> " . $sql . "</p>";
           $rs = $conn->query($sql);
           $conn.close()
				
?>
</body>
</html>
