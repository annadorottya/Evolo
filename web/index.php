<html>
<head>
<title>EVOLO</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <script src="js/jquery.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
<style>
.page-header {
 	margin: 0px 0 20px;
}

.sidebar {
	padding-right: 0px;
}

.site {
	margin-right: 0px;
}

.bg-4 { 
    background-color: #eee;
    color: #2f2f2f;
    padding-top: 20px;
    padding-bottom: 20px;
}

.macform {
	display: inline;
	width: 150px;
}
</style>

</head>
<body>
<div id="header" class="container-fluid"><a href="index.php"><img src="images/logo.png" width=200></a></div>
<div class="site row">
<div class="sidebar col-sm-2">
<div class="sidebar container-fluid">
<nav>
<ul class="nav nav-pills nav-stacked">
<li><a href="index.php"><span class="glyphicon glyphicon-home"></span> Home</a></li>
<li><a href="index.php?id=config"><span class="glyphicon glyphicon-cog"></span> Configuration</a></li>
<li><a href="index.php?id=whitelist"><span class="glyphicon glyphicon-list-alt"></span> Whitelist</a></li>
<li><a href="index.php?id=update"><span class="glyphicon glyphicon-refresh"></span> Software update</a></li>
</ul>
</nav>
</div>
</div>
<div class="col-sm-10">
<div id="main" class="container-fluid">
<?PHP
if(!isset($_GET['id']))
  $_GET['id'] = "main";
$file = $_GET['id'] . ".php";
if(file_exists($file))
  include($file);
?>
</div>
</div>
</div>
<footer class="container-fluid bg-4 text-center">
<span class="glyphicon glyphicon-copyright-mark"></span> Copyright EVOLO 2016
</footer>
</body>
</html>
