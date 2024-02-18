<!DOCTYPE html>
<html>
<head>
<style>
table {
  width: 100%;
  border-collapse: collapse;
}

table, td, th {
  border: 1px solid black;
  padding: 5px;
}

th {text-align: left;}
</style>
</head>
<body>

<!-- PHP code to establish connection with the localserver -->
<?php
require_once "../config.php"
$mysqli = new mysqli(DB_SERVER, DB_USERNAME,
                DB_PASSWORD, DB_NAME);
 
// Checking for connections
if ($mysqli->connect_error) {
    die('Connect Error (' .
    $mysqli->connect_errno . ') '.
    $mysqli->connect_error);
}
 
// SQL query to select data from database
if (isset($_GET['vehicle'])) {
	$param = $_GET['vehicle'];
	$sql = " SELECT r.v_id, r.last_reading, TIMESTAMPDIFF(MINUTE,NOW() - INTERVAL 72 HOUR, r.last_reading) as t_diff, 
	r.chan_value as volts, r2.chan_value as temp
	FROM readings r
	INNER JOIN readings r2
	ON r2.v_id = r.v_id AND r2.last_reading = r.last_reading
	WHERE r.c_id = 1 AND r2.c_id = 2 AND r.last_reading > NOW() - INTERVAL 72 HOUR AND r.v_id='$param'
	ORDER BY r.v_id ASC, r.last_reading ASC; ";
} else {
	$sql = " SELECT r.v_id, r.last_reading, TIMESTAMPDIFF(MINUTE,NOW() - INTERVAL 72 HOUR, r.last_reading) as t_diff, 
	r.chan_value as volts, r2.chan_value as temp
	FROM readings r
	INNER JOIN readings r2
	ON r2.v_id = r.v_id AND r2.last_reading = r.last_reading
	WHERE r.c_id = 1 AND r2.c_id = 2 AND r.last_reading > NOW() - INTERVAL 72 HOUR 
	ORDER BY r.v_id ASC, r.last_reading ASC; ";
}
$result = $mysqli->query($sql);

// $data = [];

// foreach ($result as $row) {
//    $data[] = $row;
// }
	
echo "<table>";
echo "<tr>";
echo "<th>V_ID</th>";
echo "<th>Reading Time (UTC)</th>";
// echo "<th>Time Diff</th>";
echo "<th>Volts</th>";
echo "<th>Temperature</th>";
echo "</tr>";
while($row=$result->fetch_assoc()){
  echo "<tr>";
  echo "<td>" . $row['v_id'] . "</td>";
  echo "<td>" . $row['last_reading'] . "</td>";
  //echo "<td>" . $row['t_diff'] . "</td>";
  echo "<td>" . $row['volts'] . "</td>";
  echo "<td>" . $row['temp'] . "</td>";
  echo "</tr>";
}
echo "</table>";

$mysqli->close();
?>
</body>
</html>
