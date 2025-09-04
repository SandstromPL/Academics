<html>
    <body>
        <?php
            $op1=$_POST["op1"];
            $op2=$_POST["op2"];
            $op=$_POST["op"];
            if(is_numeric($op1) && is_numeric($op2)){
                if($op== "+"){
                    $ans = $op1 + $op2;
                    echo "Sum is $ans .";
                }
                else if($op == "-"){
                    $ans = $op1 - $op2;
                    echo "Difference is $ans .";
                }
                else if($op == "*"){
                    $ans = $op1 * $op2;
                    echo "Product is $ans .";
                }
                else{
                    echo "<br>INVALID OPERATOR</br>";
                }
            }else{
                echo "<br>Enter valid operands!!</br>";
            }    
        ?>
    </body>
</html>