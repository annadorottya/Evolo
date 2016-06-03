<?php
file_put_contents("/home/pi/Evolo/code/whitelist.txt", $_GET['drone'].date("d/m/Y")."\n", FILE_APPEND | LOCK_EX);
?>
