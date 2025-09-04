<html>
    <body>
        <?php
           $n1 = $_POST["name"]; 
           $n2 = $_POST["email"]; 
           $n3 = $_POST["cn"]; 
           $n4 = $_POST["cty"]; 
           
           echo "<table border='1' style='width: 60%;'>";
           echo "<tr style='font-family: Arial; font-size: 20px;'>";
           echo "<th>Name</th>";
           echo "<th>Email</th>";
           echo "<th>Contact</th>";
           echo "<th>Country</th>";
           echo "</tr>";
           echo "<tr style='font-family: Arial; font-size: 16px; text-align: center;'>";
           echo "<td>$n1</td>";
           echo "<td>$n2</td>";
           echo "<td>$n3</td>";
           echo "<td>$n4</td>";
           echo "</tr>";
           echo "</table>";
        ?>
    </body>
</html>
