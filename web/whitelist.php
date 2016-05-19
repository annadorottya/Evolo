<div class="page-header"><h1>Whitelist</h1></div>
<div class="row">
	<div class="col-sm-6">

		<h2>Add new drone</h2>
			<p>Turn on the drone you want to add, and click on this button:
			<button type="button" class="btn btn-primary btn-block" data-toggle="collapse" data-target="#demo">Search for nearby drones</button></p>

			<div id="demo" class="collapse">
			<div class="alert alert-info"><span class="glyphicon glyphicon-repeat"></span> Searching for nearby drones...</div>

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
		</div>		

</div>	

			<p>Or if you have the MAC address, you can type it here:</p>
<div class="form-group">
			<form role="form" action="" method="post">
				<label for="mac">MAC address:</label><br> 
				<input type="text" maxlength="2" size="2" name="mac1" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac2" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac3" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac4" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac5" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac6" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac7" class="macform form-control"> :
				<input type="text" maxlength="2" size="2" name="mac8" class="macform form-control">
<br><br>
				<input type="submit" class="btn btn-default">
			</form>
</div>

	</div>
	<div class="col-sm-6">
		<h2>Currently whitelisted drones</h2>
		<div class="table-responsive">
			<table class="table table-striped">
				<thead>
                	<tr>
              			<th>MAC Address</th>
               			<th>Type</th>
                		<th>Date added</th>
               		</tr>
               	</thead>
               	<tbody>
                    <tr>
                        <td>00:00:00:00:00:00:00:00</td>
                        <td>AR Parrot</td>
                    	<td>01/01/2016</td>
                    </tr>
                    <tr>
             			 <td>01:00:e0:00:ff:00:32:a3</td>
             			 <td>AR Parrot</td>
              			<td>14/04/2016</td>
                	</tr>
        		</tbody>
        	</table>
		</div>
	</div>
</div>
