<?php
/*
<div class="alert alert-danger"><span class="glyphicon glyphicon-remove"></span> I didn't find any drones nearby. Please try again, moving the drone closer or type in the MAC address.</div>

			<p>I have found the following drones:</p>
		<div class="table-responsive">
			<table class="table table-striped">
				<thead>
                	<tr>
              			<th>MAC Address</th>
               			<th>Type</th>
						<th></th>
               		</tr>
               	</thead>
               	<tbody>
                    <tr>
                        <td>00:00:00:00:00:00:00:00</td>
                        <td>AR Parrot</td>
						<td><button type="button" class="btn btn-default">Add</button></td>
                    </tr>
                    <tr>
             			<td>01:00:e0:00:ff:00:32:a3</td>
             			<td>AR Parrot</td>
						<td><button type="button" class="btn btn-default">Add</button></td>
                	</tr>
        		</tbody>
        	</table>
		</div>*/
$output;
try{
$drones = "";
exec("python /home/pi/Evolo/code/listDrones.py",$output,$returnValue);
/*if(!$returnValue) die('<div class="alert alert-danger"><span class="glyphicon glyphicon-remove"></span> Error occurred while listing the drones. If persistent, contact customer service and tell them this error message: <pre>executing listDrones.py failed</pre></div>');*/
foreach($output as $line){
	if(startsWith($line,"listDrones")){
		$e = explode(";",$line);
		$drones .= '
                    <tr>
                        <td>'.$e[2].'</td>
                        <td>'.$e[1].'</td>
						<td><button type="button" class="btn btn-default" onclick="addToWhitelist(\''.$e[1].';'.$e[2].';\')">Add</button></td>
                    </tr>
';
	}
}
if($drones === ""){ //no drones found
	echo '<div class="alert alert-danger"><span class="glyphicon glyphicon-remove"></span> I didn\'t find any drones nearby. Please try again, moving the drone closer or type in the MAC address.</div>';
}else{ //drones found
	echo '<p>I have found the following drones:</p>
		<div class="table-responsive">
			<table class="table table-striped">
				<thead>
                	<tr>
              			<th>MAC Address</th>
               			<th>Wifi name</th>
						<th></th>
               		</tr>
               	</thead>
               	<tbody>' 
	. $drones .
	'</tbody>
        	</table>
		</div';
}
}
catch(Exception $e){
	echo '<div class="alert alert-danger"><span class="glyphicon glyphicon-remove"></span> Error occurred while listing the drones. If persistent, contact customer service and tell them this error message: <pre>'.$e->getMessage().'</pre></div>';
}
function startsWith($haystack, $needle) //http://stackoverflow.com/questions/834303/startswith-and-endswith-functions-in-php
{
     $length = strlen($needle);
     return (substr($haystack, 0, $length) === $needle);
}
?>
