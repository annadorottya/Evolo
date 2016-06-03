<script type="text/javascript">
var timeout;

function update(){
  if(typeof timeout !== 'undefined') clearTimeout(timeout);
  $('#updateProgressbar').css("width","0%");
  $('#updateSuccess').hide();
  $('#updateError').hide();
  $('#updateProgress').show(500);
  timeout = setTimeout(function() {updateProgressbar(1);}, 100);
}

function updateProgressbar(value){
  if(value < 101){
    $('#updateProgressbar').html(value + "%");
    $('#updateProgressbar').css("width",value + "%");
    timeout = setTimeout(function() {updateProgressbar(value+1);}, 100);
  }else{
    $('#updateProgress').hide(500);
    $('#updateSuccess').show(500);
  }
}
</script>
<div class="page-header"><h1>Update software</h1></div>

<!--<p>The current software version of your Evolo is <strong>1.8</strong>, which is the newest.-->

<p>The current software version of your Evolo is <strong>1.5</strong>, the newest version available is <strong>1.8.3</strong>. Do you want to update?</p>
<button type="button" class="btn btn-primary" onclick="update()">Update my Evolo</button>

<br><br>

<div id="updateProgress" style="display:none">
<p>Update in progress:
<div class="progress">
  <div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0"
  aria-valuemin="0" aria-valuemax="100" style="width:0%" id="updateProgressbar">
    0%
  </div>
</p>
</div>
</div>

<div class="alert alert-success" id="updateSuccess" style="display:none">
  <span class="glyphicon glyphicon-ok"></span> Update successful!
</div>

<div class="alert alert-danger" id="updateError" style="display:none">
  <span class="glyphicon glyphicon-remove"></span> Oops, something went wrong, please try again!
</div>

</div>
