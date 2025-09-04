#!/bin/bash

AF="Account.txt"
CF="Credentials.txt"

welcome_screen() {
    clear 
    echo "**** Welcome to My shellATM ****"
    echo "**** Press any key to continue ****"
    read -n 1
}

authenticate_user() {
    clear
    echo "Enter your Card Number (format: 1234 5678 1234 5678):"
    read -r card_number
    echo "Enter your Password:"
    read -r password

    if grep -q "^$card_number, $password$" "$CF"; then
        account_info=$(grep "^.*,$card_number,.*$" "$AF")
        current_balance=$(echo "$account_info" | awk -F, '{print $4}')
        user_menu
    else
        echo "Invalid Card Number or Password. Please try again."
        read -p "Press any key to retry..." -n 1
        authenticate_user
    fi
}

user_menu() {
    clear
    echo "**** Please select an option ****"
    echo "1. Withdraw cash"
    echo "2. Deposit cash"
    echo "3. Settings"
    echo "4. Exit"
    read -r option

    case $option in
        1) withdraw_cash ;;
        2) deposit_cash ;;
        3) settings ;;
        4) exit ;;
        *) echo "Invalid option. Please try again."; user_menu ;;
    esac
}

withdraw_cash() {
    clear
    echo "Enter the amount to withdraw:"
    read -r amount

    if [[ $amount =~ ^[0-9]+$ ]]; then
        if (( amount > current_balance )); then
            echo "Insufficient funds."
        else
            new_balance=$((current_balance - amount))
            sed -i "s/\($account_info,$current_balance$\)/\1,$new_balance/" "$AF"
            echo "Withdrawal successful. New balance: $new_balance"
        fi
    else
        echo "Invalid amount. Please enter a non-negative number."
    fi
    read -p "Press any key to continue..." -n 1
    user_menu
}

deposit_cash() {
    clear
    echo "Enter the amount to deposit:"
    read -r amount

    if [[ $amount =~ ^[0-9]+$ ]]; then
        new_balance=$((current_balance + amount))
        sed -i "s/\($account_info,$current_balance$\)/\1,$new_balance/" "$AF"
        echo "Deposit successful. New balance: $new_balance"
    else
        echo "Invalid amount. Please enter a non-negative number."
    fi
    read -p "Press any key to continue..." -n 1
    user_menu
}

settings() {
    clear
    echo "Enter your new email address:"
    read -r new_email

    if [[ $new_email =~ ^[a-zA-Z][a-zA-Z0-9]*@[a-z]+\.[a-z]+\.[a-z]+$ ]]; then
        sed -i "s/\($account_info,$current_balance$\)/\1,$new_email,$current_balance/" "$AF"
        echo "Email updated successfully."
    else
        echo "Invalid email format. Please try again."
    fi
    read -p "Press any key to continue..." -n 1
    user_menu
}

welcome_screen
authenticate_user

