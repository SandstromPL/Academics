<html>
    <body>
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $name = $_POST['name'];
            $email = $_POST['email'];
            $username = $_POST['username'];
            $gender = $_POST['gender'];
            $address = $_POST['address'];
            $country = $_POST['country'];
            $degrees = $_POST['degree'];
            $specialisations = $_POST['specialisation'];
            $years = $_POST['year'];
            $percentages = $_POST['percentage'];
            $hobbies = isset($_POST['hobbies']) ? implode(", ", $_POST['hobbies']) : "No hobbies selected";

            $photo_tmp = $_FILES['photo']['tmp_name'];
            $photo_name = $_FILES['photo']['name'];
            move_uploaded_file($photo_tmp, "uploads/" . $photo_name);

            $signature_tmp = $_FILES['signature']['tmp_name'];
            $signature_name = $_FILES['signature']['name'];
            move_uploaded_file($signature_tmp, "uploads/" . $signature_name);

            echo "<h2>User Information</h2>";
            echo "<table border='1' style='width: 60%; text-align: left;'>";
            echo "<tr><th>Name</th><td>$name</td></tr>";
            echo "<tr><th>Email</th><td>$email</td></tr>";
            echo "<tr><th>Username</th><td>$username</td></tr>";
            echo "<tr><th>Gender</th><td>$gender</td></tr>";
            echo "<tr><th>Address</th><td>$address</td></tr>";
            echo "<tr><th>Country</th><td>$country</td></tr>";
            
            echo "<tr><th>Education Details</th><td>";
            for ($i = 0; $i < count($degrees); $i++) {
                echo "Degree: " . $degrees[$i] . " | Specialisation: " . $specialisations[$i] . 
                    " | Year: " . $years[$i] . " | Percentage: " . $percentages[$i] . "<br>";
            }
            echo "</td></tr>";

            echo "<tr><th>Hobbies</th><td>$hobbies</td></tr>";

            echo "<tr><th>Photo</th><td><img src='uploads/$photo_name' width='100' height='100'></td></tr>";
            echo "<tr><th>Signature</th><td><img src='uploads/$signature_name' width='100' height='50'></td></tr>";
            echo "</table>";
        }
        ?>
        
    </body>
</html>