<?php 

include("db.php");

if(!isset($_GET['domain'])){
	die("no domain");
}
$domain = trim($_GET['domain']);
$outbound = trim($_GET['outbound']);

$sql = "UPDATE alexa_list SET status=2,outbound=$outbound where domain='$domain'";
$conn->query($sql);

$conn->close();
?>