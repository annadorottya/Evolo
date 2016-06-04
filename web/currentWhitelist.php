			<table class="table table-striped">
				<thead>
                	<tr>
              			<th>MAC Address</th>
               			<th>Wifi name</th>
                		<th>Date added</th>
                		<th></th>
               		</tr>
               	</thead>
               	<tbody>
<?php
$myfile = fopen("/home/pi/Evolo/code/whitelist.txt", "r") or die("Unable to open file!");
while(!feof($myfile)) {
	$line = fgets($myfile);
	$e = explode(";",$line);
	if(sizeOf($e) > 2)echo '
                  <tr>
                        <td>'.$e[1].'</td>
                        <td>'.$e[0].'</td>
                     <td>'.$e[2].'</td>
                     <td>
                       <button type="button" class="btn btn-default btn-sm" title="Delete" onclick="$.get(\'deleteFromWhitelist.php?drone=' . urlencode($line) . '\'); setTimeout(function() {window.location = window.location;}, 2000);">
                         <span class="glyphicon glyphicon-trash"></span> 
                       </button>
                    </td>
                  </tr>
';}
fclose($myfile);
?>
        		</tbody>
        	</table>
