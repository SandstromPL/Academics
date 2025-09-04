<html>
<head> </head>

<body>
<p>Guessing game...</p>
<form>
<p><label for="guess">Input Guess-1</label>
<input type="text" name="guess" id="guess"/></p>
<input type="submit"/>
</form>

<pre>
<?php
if(isset($_GET['guess'])) {
echo "Guessed value is:"; 
print_r($_GET);
}
?>
</pre>

</body>



</html>
