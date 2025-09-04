<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>PROBLEM 2</title>
    </head>
    <body>
        <h1><center>CALCULATOR</center></h1>
        <?php
            function write($op1,$op2,$ope){
                if(is_numeric($op1) && is_numeric($op2)){
                    if($ope == "+"){
                        $ans = $op1 + $op2;
                        echo "<p style='color:green;'>Sum is $ans.</p>";
                    }else if($ope == "-"){
                        $ans = $op1 - $op2;
                        echo "<p style='color:green;'>Difference is $ans.</p>";
                    }else if($ope == "*"){
                        $ans = $op1 * $op2;
                        echo "<p style='color:green;'>Product is $ans.</p>";
                    }else{
                        echo "<p style='color:red;'>Invalid operator.</p>";
                    }
                }else{
                    echo "<p style='color:red;'>Enter valid inputs.</p>";
                }
            }

            if( $_SERVER["REQUEST_METHOD"] == "POST"){
                $op1 = $_POST['op1'] ?? '';
                $op2 = $_POST['op2'] ?? '';
                $operator = $_POST['operator'] ?? '';

                write($op1,$op2,$operator);
            }
        ?>

        <form action="" method="post">
            <label for="op1">OP1:</label>
            <input type="text" id="op1" name="op1" required><br><br>
            <label for="op2">OP2:</label>
            <input type="text" id="op2" name="op2" required><br><br>
            <label for="operator">OPERATOR:</label>
            <input type="text" id="operator" name="operator" required><br><br>
            <input type="submit" value="SUBMIT">
            
        </form>
    </body>
</html>