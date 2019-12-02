<?php 

include("db.php");


$sql = "SELECT domain FROM alexa_list where status=0 ORDER BY alexa_list_id limit 0,100;";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
	$domains = $result->fetch_assoc();
    while($row = $result->fetch_assoc()) {
        echo $row["domain"]." ";
    }
	$sql = "UPDATE alexa_list SET status=1 WHERE domain IN ('".implode("','",$domains)."')";
	$conn->query($sql);
}


$conn->close();
?>