import random
import sys
import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS card(
                    id INTEGER NULL PRIMARY KEY AUTOINCREMENT,
                    number TEXT,
                    pin TEXT,
                    balance INTEGER DEFAULT 0
                );
                """)

conn.commit()

run = True


def menu():
    print("1. Create an account\n2. Log into account\n0. Exit")


def menu2():
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")


def transfer_money(self):
    print("\nTransfer\nEnter card number:")
    transfer_card = input()
    dbl_check = self.luhn(transfer_card)
    if dbl_check is False:
        print("Probably you made mistake in the card number. Please try again!\n")
    elif (transfer_card,) not in c.execute('SELECT number FROM card;').fetchall():
        print("Such a card does not exist.\n")
        menu2()
    elif transfer_card == self.account:
        print("You can't transfer money to the same account!")
        menu2()
    else:
        print("Enter how much money you want to transfer:")
        to_transfer = input()
        balance_check = c.execute(f'SELECT balance FROM card WHERE number = {self.account};').fetchone()
        balance_check = ''.join(map(str, balance_check))
        if int(to_transfer) > int(balance_check):
            print("Not enough money!\n")
        else:
            print("Success!\n")
            c.execute(f'UPDATE card SET balance = balance - {to_transfer} WHERE number = {self.account};')
            c.execute(f'UPDATE card SET balance = balance + {to_transfer} WHERE number = {transfer_card};')
            conn.commit()


class ATM:
    cards = {}

    def __init__(self):
        self.card_number = None
        self.pin = None
        self.running = True
        self.balance = 0
        self.account = 0
        self.run()

    def create_card(self):
        while run:
            self.card_number = "400000" + str(random.randint(000000000, 999999999)) + str(random.randint(0, 9))
            self.pin = random.randint(0000, 9999)
            self.pin = str(self.pin).zfill(4)
            if len(self.card_number) == 16 and self.luhn(self.card_number):
                self.cards.update({self.card_number: self.pin})
                c.execute("INSERT INTO card VALUES (NULL,?,?,?)",
                          (str(self.card_number), str(self.pin), str(self.balance)))
                conn.commit()
                print("\nYour card has been created\nYour card number: \n{0}\nYour card PIN: \n{1}\n".format(
                    self.card_number, self.pin))
                menu()
                return self.card_number, self.pin
            else:
                continue

    def after_login(self):
        menu2()
        while self.run:
            command_input = input("")
            if command_input == "1":
                query = c.execute(f'SELECT balance FROM card WHERE number = {self.account}').fetchone()
                print("\nBalance:",int(query[0]), "\n")
                menu2()
                continue
            if command_input == "2":
                balance_input = input("\nEnter income: \n")
                c.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (balance_input, self.account))
                conn.commit()
                print("Income was added!\n")
                menu2()
                continue
            if command_input == "3":
                transfer_money(self)
                menu2()
                continue
            elif command_input == "4":
                c.execute(f"DELETE FROM card WHERE number = {self.account}").fetchone()
                conn.commit()
                print("\nThe account has been closed!\n")
                menu()
                break
            elif command_input == "5":
                print("\nYou have successfully logged out!")
                menu()
                break
            elif command_input == "0":
                print("Bye!")
                sys.exit()

    def check_login(self):
        check_login = input("\nEnter your card number: \n")
        check_pin = input("Enter your PIN: \n")
        c.execute(f'SELECT number, pin, balance FROM card WHERE number = {check_login}')
        result = c.fetchone()
        try:
            if len(check_login) != 16 or len(check_pin) != 4 or result is None or check_pin != result[1]:
                print('Wrong card number or PIN!\n')
                menu()
                return False
            else:
                print('You have successfully logged in!\n')
                self.account = check_login
                self.after_login()
                return True
        except ValueError:
            print("None happened")

    def run(self):
        menu()
        while self.running:
            command_input = input()
            if command_input == "1":
                self.create_card()
            elif command_input == "2":
                self.check_login()
            elif command_input == "0":
                print("Bye!")
                conn.close()
                sys.exit()

    def luhn(self, card_number):
        sum = 0
        num_digits = len(card_number)
        oddeven = num_digits & 1
        for count in range(0, num_digits):
            digit = int(card_number[count])
            if not ((count & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            sum = sum + digit
        if sum % 10 == 0:
            return True
        else:
            return False


ATM()
