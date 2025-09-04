<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title><>PROBLEM 3</title>
    </head>
    <body>
        <h1><center>USER INFO</center></h1>
        <?php
            $program="BTech";
            $department="cSe";
            $cnt=10;
            echo "<table border='1'>";
            echo "<tr>";
            echo "<th>Roll No</th>";
            echo "<th>UserName</th>";
            echo "<th>EmailID</th>";
            echo "<th>ID Number</th>";
            echo "</tr>";
            for($i= 1; $i <= $cnt; $i++){
                echo "<tr>";
                echo "<th>$i</th>";
                echo "<th>$department _ $i</th>";
                echo "<th>$department _ $i@iitbhilai.ac.in</th>";
                echo "<th>$program _ $department _ $i</th>";
                echo "</tr>";
            }
            echo "</table>";
        ?>
    </body>
</html>