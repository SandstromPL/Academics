<html>
<head> </head>

<body>

<form>
<p><label for="inp06">Which soda:
<select name="soda" id="inp06">
<option value="0">-- Choose the option --</option>
<option value="1">Coke</option>
<option value="2">Pepsi</option>
<option value="3">Mountain Dew</option>
<option value="4">Orange Juice</option>
<option value="5">Lemonade</option>
</select>
<input type="submit"/>
</p>

</form>

<pre>
<?php
if(isset($_GET['soda'])) {
	echo "SODA value is ".$_GET['soda'];
	echo "<br>";
}
?>
</pre>
</body>
</html>
