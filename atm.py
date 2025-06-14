import sqlite3
import account


class ATM(account.Account):
    __bank_name = "Muath Bank"
    def __init__(self, uid, name, age, username, password, acc_id, balance=0):
        super().__init__(uid, name, age, username, password)
        self.__balance = balance
        self.__acc_id = acc_id
        self.__transaction = [] # list to store list of transactions.
        self.friends = [] # list to store dicts of friends.
    def withdrawal(self, amount):
        self.__balance -= amount
        print(f"\n{amount}SAR has been withdrawn successfully.")
        print("New balance: ", self.__balance)
        self.__transaction.append(f"{amount}SAR has been withdrawn successfully.")
        self.update_balance()
    def deposit(self, amount):
        self.__balance += amount
        print(f"\n{amount}SAR has been deposited successfully.")
        print ("New balance: ", self.__balance)
        self.__transaction.append(f"{amount}SAR has been deposited successfully.")
        self.update_balance()
    def set_acc_id(self, acc_id):
        self.__acc_id = acc_id
        print(f"Account number has been changed to {acc_id} successfully.")
    def set_balance(self, new_balance):
        self.__balance = new_balance
        print(f"Your balance now is: {new_balance}")
    def get_acc_id(self):
        return self.__acc_id
    def get_balance(self):
        return self.__balance
    def set_friends(self, acc_id, name):
        self.friends.append({"name":name, "acc_id":acc_id}) # append a dict of a friend to the friends list.
        print("Friend has been added successfully.")
        self.__transaction.append(f"Friend \"{name}\" has been added successfully.")
        self.update_balance()
    def get_friends(self):
        return self.friends
    def transfer(self, amount, acc_num):
        self.__balance -= amount
        print (f"\n{amount}SAR has been transformed to account number {acc_num} successfully.")
        print ("New balance: ", self.__balance)
        self.__transaction.append(f"{amount}SAR has been transformed to account number {acc_num} successfully.")
        self.update_balance()
    def display(self):
        super().display()
        print("Account ID:", self.__acc_id)
        print("balance:", self.__balance)
    def get_bank_name(self):
        return self.__bank_name
    def set_transaction_history(self, message):
        self.__transaction.append(message)
    def get_transaction_history(self):
        return self.__transaction
    def update_balance(self):
        ATM_db = sqlite3.connect("ATM.db")
        cur = ATM_db.cursor()
        cur.execute("UPDATE users SET balance = ? WHERE id = ?", (self.__balance, self.get_id()))
        ATM_db.commit()
        ATM_db.close()