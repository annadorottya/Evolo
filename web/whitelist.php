<script type="text/javascript">
function formatMAC() {
    var macAddress = $("#macAddress");
    var r = /([a-f0-9]{2})([a-f0-9]{2})/i,
        str = macAddress.val().replace(/[^a-f0-9]/ig, "");
    
    while (r.test(str)) {
        str = str.replace(r, '$1' + ':' + '$2');
    }

    macAddress.val(str.slice(0, 17));
};

function addToWhitelistByMac() {
	var macAddress = $("#macAddress");
	addToWhitelist("<i>Added with MAC</i>;" + macAddress.val() + ";");
}

function addToWhitelist(drone) {
	$.get("addToWhitelist.php?drone=" + drone);
	setTimeout(function() {window.location = window.location;}, 1000);
}
</script>

<div class="page-header"><h1>Whitelist</h1></div>
<div class="row">
	<div class="col-sm-6">

		<h2>Add new drone</h2>
			<p>Turn on the drone you want to add, and click on this button:
			<button type="button" class="btn btn-primary btn-block" data-toggle="collapse" data-target="#demo" onclick='$("#listDrones").val("<div class=\"alert alert-info\"><span class=\"glyphicon glyphicon-repeat\"></span> Searching for nearby drones...</div>"); $("#listDrones").show(); $("#listDrones").load("listDrones.php");'>Search for nearby drones</button></p>

			<div id="listDrones" class="collapse">
			<div class="alert alert-info"><span class="glyphicon glyphicon-repeat"></span> Searching for nearby drones...</div>
			</div>
			<!--<div class="alert alert-danger"><span class="glyphicon glyphicon-remove"></span> I didn't find any drones nearby. Please try again, moving the drone closer or type in the MAC address.</div>

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
		</div>-->

		</div>

			<p>Or if you have the MAC address, you can type it here:</p>
<div class="form-group">
			<form role="form" action="" method="post">
				<label for="mac">MAC address:</label><br> 
				<input type="text" maxlength="17" size="17" name="macAddress" id="macAddress" class="macform form-control" onkeyup="formatMAC()">
<br><br>
				<input type="submit" class="btn btn-default" value="Add to whitelist" onclick="addToWhitelistByMac()">
			</form>
</div>

	</div>
	<div class="col-sm-6">
		<h2>Currently whitelisted drones</h2>
		<div class="table-responsive" id="currentWhitelist">
<?php include('currentWhitelist.php'); ?>
		</div>
	</div>
</div>
