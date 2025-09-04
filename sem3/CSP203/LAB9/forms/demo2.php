<html>
<head> </head>

<body>
<p>Preferred Time:<br/>
<form>

<input type="radio" name="when" value="AMISPASSED">AM<br>
<input type="radio" name="when" value="pm" checked>PM
<input type="submit"/>
</p>
</form>

<pre>
<?php
if(isset($_GET['when'])) {
echo "Time is ".$_GET['when'];
}
?>
</pre>

</body>



</html>
