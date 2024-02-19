<?php
/* MySQL Database credentials.
//server with default setting (user 'root' with no password) */

require_once('config.php');

$conn = new mysqli(DB_SERVER, DB_USERNAME,
                DB_PASSWORD, DB_NAME);
                
// Checking for connections
if ($mysqli->connect_error) {
    die('Connect Error (' .
    $mysqli->connect_errno . ') '.
    $mysqli->connect_error);
}

?>
