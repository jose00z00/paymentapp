import streamlit as st
from streamlit_option_menu import option_menu
import base64
import json

class Account:
    def __init__(self, name, card_number, pin, phone_numbers):
        self.name = name
        self.card_number = card_number
        self.pin = pin
        self.phone_numbers = phone_numbers
        self.balance = 100000  
        self.charge = 0 

def save_data(accounts):
    with open('data.json', 'w') as file:
        data = {'accounts': []}
        for account in accounts:
            data['accounts'].append({
                'name': account.name,
                'card_number': account.card_number,
                'pin': account.pin,
                'phone_numbers': account.phone_numbers,
                'balance': account.balance,
                'charge': account.charge
            })
        json.dump(data, file, indent=6)

def load_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            accounts = []
            for account_data in data['accounts']:
                accounts.append(Account(account_data['name'], account_data['card_number'], account_data['pin'], account_data['phone_numbers']))
                accounts[-1].balance = account_data['balance']
                accounts[-1].charge = account_data['charge']

            return accounts
    except FileNotFoundError:
        return []

def register_account(accounts):
    name = st.text_input("Enter your name:")
    card_number = st.text_input("Enter your card number:")
    pin = st.text_input("Enter your PIN:", type="password")
    phone_number = st.text_input("Enter your phone number:")
    if st.button("Register Account"):
        for account in accounts:
            if account.card_number == card_number:
                st.error("This card number is already registered.")
                return
            if phone_number in account.phone_numbers:
                st.error("This phone number is already registered.")
                return
        accounts.append(Account(name, card_number, pin, [phone_number])) 
        st.success("Account registered successfully!")
        save_data(accounts)

def register_simcard(accounts):
    st.write("to register a new phone number you should have an already registered card number! if you dont you cant add a new phone number.")
    new_number = st.text_input("Enter your new phone number:")
    card_number = st.text_input("Enter your card number:")
    if st.button("Confirm"):
        notregistered=True
        for account in accounts:
            if account.card_number == card_number and new_number not in account.phone_numbers:
                notregistered=False
                account.phone_numbers.append(new_number)
                save_data(accounts)
                st.success("You registered your new number successfully")
                break
        if notregistered:
             st.error("the card you entered isnt registered or the number is an already registered one!")
              


def charge_phone(accounts):
    card_number = st.text_input("Enter your card number:")
    phone_number = st.text_input("Enter your phone number:")
    amount = st.number_input("Enter the amount to charge your phone:", min_value=0)
    pin = st.text_input("Enter your PIN:", type="password")
    if st.button("Confirm your purchase"):
        for account in accounts:
            if account.card_number == card_number and phone_number in account.phone_numbers:
                if account.pin == pin:
                    if account.balance >= amount:
                        account.balance -= amount
                        account.charge += amount
                        st.success("Phone charged successfully!")
                        save_data(accounts)
                        return
                    else:
                        st.error("Insufficient balance!")
                        return
                else:
                    st.error("Invalid PIN!")
                    return
        st.error("Invalid card number or phone number!")

def transfer(accounts):
    sender_card_number = st.text_input("Enter sender's card number:")
    receiver_card_number = st.text_input("Enter receiver's card number:")
    amount = st.number_input("Enter the amount to transfer:", min_value=0)
    if amount :
        sender_pin = st.text_input("Enter your PIN:", type="password")
    if st.button("Transfer"):
        recex=False
        for account in accounts:
            if account.card_number == receiver_card_number:
                receiver=account
                recex=True
                break
        notregistered=True
        if recex :
          for account in accounts:
              if account.card_number == sender_card_number:
                  notregistered=False
                 
                  if account.pin == sender_pin:
                    
                     if account.balance >= amount:
                         account.balance -= amount
                         receiver.balance += amount

                         st.success("Transfer successful!", icon='🔥')
                         save_data(accounts)
                         return
                     else:
                          st.error("Insufficient balance!")
                          return
                  
                  st.error("Invalid PIN!")
                       
        elif notregistered:
           st.error("in order to transfer money you should register both sender's and receiver's card numbers first")

def check_balance(accounts):
    card_number = st.text_input("Enter your card number:")
    pin = st.text_input("Enter your PIN:", type="password")
    if st.button("Check Balance"):
        for account in accounts:
            if account.card_number == card_number and account.pin == pin:
                st.info(f"Your current balance is: {account.balance}")
                return
        st.error("Invalid card number or PIN!")





def main():
    st.title("Payment App")

    accounts = load_data()
    

    with st.sidebar:
       main_menu = option_menu("Main Menu", ["Register Account", "Register Another Phone Number", "Charge Phone", "Transfer", "Check Balance"],
         default_index=1)
       main_menu
    
    if main_menu == "Register Account":
        register_account(accounts)
    elif main_menu == "Register Another Phone Number":
        register_simcard(accounts)
    elif main_menu == "Charge Phone":
        charge_phone(accounts)
    elif main_menu == "Transfer":
        transfer(accounts)
    elif main_menu == "Check Balance":
        check_balance(accounts)

if __name__ == "__main__":
    main()
