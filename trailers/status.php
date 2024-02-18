<!-- PHP code to establish connection with the localserver -->
<?php

require_once "config.php"
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
$mysqli->close();
?>

<!-- HTML code to display data in tabular format -->
<!DOCTYPE html>
<html lang="en">
 
<head>
    <meta charset="UTF-8">
    <title>MITRU Status Data</title>
    <!-- CSS FOR STYLING THE PAGE -->
    <style>
        table {
            margin: 0 auto;
            font-size: large;
            border: 1px solid black;
        }
 
        h1 {
            text-align: center;
            color: #006600;
            font-size: xx-large;
            font-family: 'Gill Sans', 'Gill Sans MT',
            ' Calibri', 'Trebuchet MS', 'sans-serif';
        }
 
        td {
            background-color: #E4F5D4;
            border: 1px solid black;
        }
 
        th,
        td {
            font-weight: bold;
            border: 1px solid black;
            padding: 10px;
            text-align: center;
        }
 
        td {
            font-weight: lighter;
        }
    </style>
</head>
 
<body>
    <section>
        <h1>Mitru Status Data</h1>
        <!-- TABLE CONSTRUCTION -->
        <table>
            <tr>
                <th>v_id</th>
                <th>Last Update</th>
                <th>Time Diff</th>
				<th>Battery Voltage</th>
				<th>Temperature</th>
            </tr>
            <!-- PHP CODE TO FETCH DATA FROM ROWS -->
            <?php
                // LOOP TILL END OF DATA
                while($rows=$result->fetch_assoc())
                {
            ?>
            <tr>
                <!-- FETCHING DATA FROM EACH
                    ROW OF EVERY COLUMN -->
                <td><?php echo $rows['v_id'];?></td>
                <td><?php echo $rows['last_reading'];?></td>
                <td><?php echo $rows['t_diff'];?></td>
				<td><?php echo $rows['volts'];?></td>
				<td><?php echo $rows['temp'];?></td>
            </tr>
            <?php
                }
            ?>
        </table>
    </section>
</body>
 
</html>
