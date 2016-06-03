<?php
$contents = file_get_contents("/home/pi/Evolo/code/whitelist.txt");
$contents = str_replace(urldecode($_GET["drone"]), '', $contents);
file_put_contents("/home/pi/Evolo/code/whitelist.txt", $contents);
?>
