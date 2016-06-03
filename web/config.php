<div class="page-header"><h1>Configuration</h1></div>

<p>Here you can configure the settings of your Evolo.</p>
<div class="row">
	<div class="col-sm-6">
	<h2>Adjust range</h2>
	<div class="form-group">
	<p>
	  <span style="float: left">10%</span>
	  <span style="float: right">100%</span>
	</p>
	<input type="range" min="10" max="100" step="5" value="<?php echo intval(file_get_contents("/home/pi/Evolo/code/range.txt")); ?>" name="range" id="range"><br>
	<input type="submit" class="btn btn-default" value="Save" onclick="$.get('adjustRange.php?range=' + $('#range').val()); $('#message').hide(); $('#message').val('<div class=\'alert alert-success\'><span class=\'glyphicon glyphicon-ok\'></span> Range updated</div>'); $('#message').show();">
	</div>
	<div id="message"></div>
		</div>
		<!--<div class="col-sm-6">
			<h2>Something else</h2>
		</div>-->
</div>
