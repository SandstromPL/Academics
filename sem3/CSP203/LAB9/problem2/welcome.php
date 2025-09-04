<html>
    <body>
        <?php
            if($_GET["username"] == "csp203" && $_GET["password"] == "csp203"){
                echo "Login is successful.";
            }else{
                echo "Login is unsuccessful.";
            }
        ?>
    </body>
</html>