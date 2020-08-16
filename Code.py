import random
import sys
import sqlite3

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS card (
             id INTEGER,
             number TEXT,
             pin TEXT,
             balance INTEGER DEFAULT 0
            );
            ''')


class SimpleBankingSystem:

    def __init__(self):
        self.card_num = None
        self.pin_code = None
        self.balance = 0

        self.card_1 = None
        self.card_2 = None
        self.checksum = None

        self.user_choice = None
        self.user_login = None
        self.user_password = None

        self.user_after_log_in = None
        self.income_num = None
        self.transfer_1 = None
        self.transfer_num = None

        self.only_one = None
        self.only_two = None

    def create_an_account(self):
        self.create_card_num()
        self.create_pin()
        cur.execute(f'''INSERT INTO card
        VALUES (1, {self.card_num}, {self.pin_code}, 0)''')
        conn.commit()
        print(f"""
Your card has been created
Your card number:
{self.card_num}
Your card PIN:
{self.pin_code}
""")
        self.main_menu()

    def check_luhn(self):
        self.card_2 = [int(x) for x in self.transfer_1]
        for i in range(1, 16):
            if i % 2 != 0:
                self.card_2[i - 1] *= 2
                if self.card_2[i - 1] > 9:
                    self.card_2[i - 1] -= 9
        if sum(self.card_2) % 10 != 0:
            print('Probably you made mistake in the card number. Please try again!\n')
            self.after_log_in_menu()
        else:
            pass

    def create_card_num(self):
        while True:
            self.card_1 = str(400000) + str(random.randint(100000000, 999999999))
            self.card_2 = [int(x) for x in self.card_1]
            for i in range(1, 16):
                if i % 2 != 0:
                    self.card_2[i - 1] *= 2
                    if self.card_2[i - 1] > 9:
                        self.card_2[i - 1] -= 9
            for n in range(1, 11):
                if (sum(self.card_2) + n) % 10 == 0:
                    self.checksum = n
                    break
                else:
                    pass
            self.card_num = self.card_1 + str(self.checksum)
            if len(self.card_num) != 16:
                continue
            else:
                break

    def create_pin(self):
        self.pin_code = random.randint(1000, 9999)

    def income(self):
        print('\nEnter income:\n')
        self.income_num = int(input())
        cur.execute(f'UPDATE card SET balance = balance + {self.income_num} WHERE number = {str(self.user_login)}')
        conn.commit()
        print('Income was added!\n')
        self.after_log_in_menu()

    def transfer(self):
        print('\nTransfer')
        self.transfer_1 = input('Enter card number:\n')
        self.check_luhn()
        cur.execute('SELECT number FROM card')
        self.only_one = cur.fetchall()
        if self.transfer_1 == self.user_login:
            print("You can't transfer money to the same account!")
            self.after_log_in_menu()
        elif (self.transfer_1,) not in self.only_one:
            print('Such a card does not exist.\n')
            self.after_log_in_menu()
        else:
            self.transfer_num = int(input('Enter how much money you want to transfer:\n'))
            cur.execute(f'SELECT balance FROM card WHERE number = {str(self.user_login)}')
            self.only_one = cur.fetchone()
            if self.transfer_num > self.only_one[0]:
                print('Not enough money!')
                self.after_log_in_menu()
            else:
                cur.execute(f'UPDATE card SET balance = balance - {self.transfer_num} WHERE number = {str(self.user_login)}')
                conn.commit()
                cur.execute(f'UPDATE card SET balance = balance + {self.transfer_num} WHERE number = {str(self.transfer_1)}')
                conn.commit()
                print('Success!\n')
                self.after_log_in_menu()

    def close_account(self):
        cur.execute(f'DELETE FROM card WHERE number = {str(self.user_login)}')
        conn.commit()
        print('\nThe account has been closed!\n')
        self.main_menu()

    def after_log_in_menu(self):
        while True:
            print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
''')
            self.user_after_log_in = int(input())
            if self.user_after_log_in == 1:
                print(f"\nBalance: {self.balance}\n")
                continue
            elif self.user_after_log_in == 2:
                self.income()
            elif self.user_after_log_in == 3:
                self.transfer()
            elif self.user_after_log_in == 4:
                self.close_account()
            elif self.user_after_log_in == 5:
                print("\nYou have successfully logged out!\n")
                self.main_menu()
            elif self.user_after_log_in == 0:
                sys.exit()

    def log_in(self):
        print('\nEnter your card number:')
        self.user_login = input()
        print('Enter your PIN:')
        self.user_password = input()
        cur.execute(f'SELECT number FROM card WHERE number = {self.user_login};')
        self.only_one = cur.fetchone()
        cur.execute(f'SELECT pin FROM card WHERE number = {self.user_login};')
        self.only_two = cur.fetchone()
        if (self.user_login,) != self.only_one or (self.user_password,) != self.only_two:
            print('\nWrong card number or PIN!\n')
            self.main_menu()
        elif (self.user_login,) == self.only_one and (self.user_password,) == self.only_two:
            print('\nYou have successfully logged in!\n')
            self.after_log_in_menu()

    def main_menu(self):
        while True:
            print('''1. Create an account
2. Log into account
0. Exit''')
            self.user_choice = int(input())
            if self.user_choice == 1:
                self.create_an_account()
            elif self.user_choice == 2:
                self.log_in()
            elif self.user_choice == 0:
                sys.exit()


bank = SimpleBankingSystem()
bank.main_menu()
