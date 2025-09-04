<html>
<head> </head>

<body>

<form>
<p>Classes taken:<br/>
<input type="checkbox" name="class1" value="si502"
checked>
SI502 - Networked Tech<br>
<input type="checkbox" name="class2" value="si539">
SI539 - App Engine<br>
<input type="checkbox" name="class3">
SI543 - Java<br>
<input type="submit"/>
</p>
</form>

<pre>
<?php
if(isset($_GET['class1'])) {
	echo "Class 1 value is is ".$_GET['class1'];
	echo "<br>";
}
if(isset($_GET['class2'])) {
	echo "Class 2 is value ".$_GET['class2'];
	echo "<br>";
}
if(isset($_GET['class3'])) {
	echo "Class 3 value is ".$_GET['class3'];
	echo "<br>";
}
?>
</pre>
</body>
</html>
