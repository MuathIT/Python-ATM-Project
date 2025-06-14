import re
import random
import sqlite3
import atm

def get_cursor(): # opens the db file and return the connection variable with its cursor (but you need to commit and close manually).
    ATM_db = sqlite3.connect("ATM.db")
    return  ATM_db.cursor(), ATM_db

def create_table():
    cur, ATM_db = get_cursor()
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS Users(
                        id INT PRIMARY KEY,
                        name TEXT NOT NULL, 
                        age INTEGER CHECK(age BETWEEN 18 AND 100), 
                        username TEXT UNIQUE NOT NULL, 
                        password TEXT NOT NULL,
                        acc_id INTEGER NOT NULL,
                        balance REAL DEFAULT 0
                        )""")
    ATM_db.commit()
    ATM_db.close()

def add_user(user):
    uID = user.get_id()
    name = user.get_name()
    age = user.get_age()
    uname = user.get_username()
    pwd = user.get_password()
    acc_id = user.get_acc_id()
    balance = user.get_balance()
    if not check_user_already_added(uID):
        cur, ATM_db = get_cursor()
        cur.execute("INSERT INTO Users VALUES (?,?,?,?,?,?,?)", (uID, name, age, uname, pwd, acc_id, balance))
        ATM_db.commit()
        ATM_db.close()
    else:
        print("This user is already registered.")

def show_user(uid):
    cur, ATM_db = get_cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (uid,))
    data = cur.fetchone()
    if data:
        print("ID:", data[0])
        print("Name:", data[1])
        print("Age:", data[2])
        print("Username:", data[3])
        print("Password:", data[4])
        print("Account number:", data[5])
    else:
        print("User not found.")
    ATM_db.commit()
    ATM_db.close()

def delete_user (uid):
    admins_ids = [1] # A list stores the admins or users ids which cannot be deleted.
    if uid in admins_ids:
        print("This user cannot be deleted.")
        return
    cur, ATM_db = get_cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (uid,))
    ATM_db.commit()
    ATM_db.close()
    print("User deleted.")
    show_users()

def display_balance(user):

    print("\nBalance:", user.get_balance())

def is_strong_password(password):
    if len(password) < 8:
        print ("Sorry, your password is less than 8 characters")
        return False
    elif not re.search(r"\d", password):
        print("Sorry, your password doesn't have digits.")
        return False
    elif re.search(r"\s", password):
        print("Sorry, your password have spaces.")
        return False
    elif not re.search(r"[A-Z]", password):
        print("Sorry, your password doesn't have uppercase letters.")
        return False
    elif not re.search(r"[!@#$%^&*{}:<>?/.~,]", password):
        print("Sorry, your password doesn't have symbols.")
        return False
    else:
        return True

def take_amount():
    while True:
        user_input = input("Enter the amount (Q/q to exit): ")
        if check_exit(user_input) is None:
            return None
        try:
            amount = float(user_input)
            if amount > 0:
                return amount
            else:
                print("Sorry, the amount should be greater than 0.")
        except ValueError:
            print("Sorry, please enter a valid amount.")

def take_account_id(user):
    while True:
        try:
            user_input = input("Enter the account number (Q/q to exit): ")
            if check_exit(user_input) is None:
                return None
            acc = int(user_input)
            for account in user.get_friends():
                if account["acc_id"] == acc:
                    return acc
            else:
                print("Sorry. You don't have this account in your friends list.")
        except ValueError:
            print("Sorry, please enter a valid account number.")

def deposit(user):
    amount = take_amount()
    if amount is None:
        print("Operation has been cancelled.")
    else:
        user.deposit(amount)

def withdrawal(user):
    while True:
        display_balance(user)
        amount = take_amount()
        if amount is None:
            print("Operation has been cancelled.")
            break
        elif amount > user.get_balance():
            print ("Sorry, you don't have this amount of money.")
        else:
            user.withdrawal(amount)
            break

def transfer(user):
    while True:
        display_balance(user)
        amount = take_amount()
        if amount is None:
            print("Operation has been cancelled.")
            return None
        elif amount > user.get_balance():
            print("Sorry, you don't have this amount of money.")
        else:
            acc_id = take_account_id(user)
            if acc_id is None:
                return None
            else:
                user.transfer(amount, acc_id)
                break

def get_valid_id():
    while True:
        uid = input("Enter the ID (Q/q to exit): ")
        if check_exit(uid) is None:
            return None
        else:
            try:
                uid = int(uid)
                if not check_user_already_added(uid):
                    return uid
                else:
                    print("The ID is already taken.")
            except ValueError:
                print("Invalid input, please enter a number.")

def get_valid_name():
    while True:
        name = input("Enter a name(Q/q to exit): ")
        if check_exit(name) is None:
            return None
        if len(name) > 0:
            return name.capitalize()
        else:
            print("Sorry, please enter a valid name.")

def get_valid_age():
    while True:
        try:
            user_input = input("Enter the age(Q/q to exit): ")
            if check_exit(user_input) is None:
                return None
            age = int(user_input)
            if age >= 18:
                return age
            else:
                print("Sorry, age must be bigger than 18.")
        except ValueError:
            print("Sorry, please enter a valid age.")

def get_valid_username():
    while True:
        username = input("Enter a username(Q/q to exit): ")
        if check_exit(username) is None:
            return None
        if check_duplicated_username(username) is not None: # Checks if the username in the dict = is already taken.
            print("Sorry, this username is taken. Please try another one.")
            continue
        if len(username) > 0: # Checks if the user didn't write anything.
            return username
        else:
            print("Sorry, please enter a valid username.")

def get_strong_password(username): # Prompt the user to enter the password.
    while True:
            password = input("Enter a password (at least 8 characters)(Q/q to exit): ")
            if check_exit(password) is None:
                return None
            if password == username:
                print("You can't enter the username as a password.")
                continue
            if is_strong_password(password): # if the password is strong = break the loop and return the password.
                return password

def take_choice(user): # Prompt the user to enter a choice from the options list.
    while True:
        option = input("\nEnter your choice:\n1-Deposit.\n2-Withdrawal.\n3-Transfer.\n4-Show balance.\n5-Show friends."
                       "\n6-Add friend.\n7-Remove friend.\n8-Search for a friend.\n9-Show transaction history."
                       "\n10-Sittings.\n\n(Q/q)-Exit\n")
        if check_exit(option) is None:
            print(f"Thank you for using {user.get_bank_name()} :)")
            return None
        try:
            choice = int(option)
            if choice == 10 and user.get_id() == 1:
                admin_sittings()
            else:
                check_valid_choice(user, choice)
        except ValueError:
            print("Invalid input. Please enter a number.")

def check_valid_choice(user, choice): # Direct the list of the operations in the app.
    choices = {
            1: lambda : deposit(user),
            2: lambda : withdrawal(user),
            3: lambda : transfer(user),
            4: lambda : display_balance(user),
            5: lambda : show_friends(user),
            6: lambda : add_friends(user),
            7: lambda : remove_friends(user),
            8: lambda : search_friends(user),
            9: lambda : show_transaction_history(user),
            10: lambda : user_sittings(user)
    }

    action = choices.get(choice)
    if action:
        action()
    else:
        print("Please enter an option from the list.")

def check_login(): # Checks if the username and password are correct.
    cur, ATM_db = get_cursor()
    while True:
        uname = input("Username(Q/q to exit): ")
        if check_exit(uname) is None:
            return None

        pwd = input("Password(Q/q to exit): ")
        if check_exit(pwd) is None:
            return None

        # print(f"Entered: {uname} / {pwd}")
        # print(f"Stored:  {users[uname].get_username()} / {users[uname].get_password()}")

        # if uname in users and users[uname].get_password() == pwd:
        #     return users[uname]
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (uname, pwd))
        data = cur.fetchone()
        if data:
            uid, name, age, username, password, acc_id, balance = data
            return atm.ATM(uid, name, age, username, password, acc_id, balance)
        else:
            print("Invalid user or password, Please try again.")

def check_exit(user_input): # Checks if the user wants to exit the current interface.
    if user_input.lower() == 'q':
        return None
    else:
        return user_input

def check_duplicated_username(uname):
    cur, ATM_db = get_cursor()
    cur.execute("SELECT username FROM Users WHERE username = ?", (uname,))
    data = cur.fetchall()
    ATM_db.commit()
    ATM_db.close()
    if data:
        return not None

def check_duplicated_acc_id(acc_id):
    cur,ATM_db = get_cursor()
    cur.execute("SELECT acc_id FROM Users WHERE acc_id = ?", (acc_id,))
    data = cur.fetchone()
    ATM_db.commit()
    ATM_db.close()
    if data:
        return not None

def take_user():# Creates the account.
    while True:
        uid = random.randint(2,999)
        acc_id = random.randint(10000, 99999)
        if check_user_already_added(uid) is None and check_duplicated_acc_id(acc_id) is None:
            break
    name = get_valid_name()
    if name is None:
        return None
    age = get_valid_age()
    if age is None:
        return None
    username = get_valid_username()
    if username is None:
        return None
    password = get_strong_password(username)
    if password is None:
        return None

    users_dict[username] = atm.ATM(uid, name, age, username, password, acc_id)
    add_user(users_dict[username])
    print("\nAccount has been created successfully.")

def want_open(): # prompt the user choose login or register.
    while True:
        print(f"\n-----Welcome to Muath Bank-----")
        try:
            login_or_register = input("\nPlease enter the number that specify what you want:\n1-Register\n2-Login"
                               "\n\n(Q/q to exit)\n")

            if check_exit(login_or_register) is None: # if the user entered 'q'
                return None

            login_or_register = int(login_or_register) # convert the variable to int.
            if login_or_register in range(0, 3): # if the user entered 0, 1 or 2
                return login_or_register
            else:
                print("Sorry, please enter a valid choice.")

        except ValueError:
            print("Sorry, please enter a valid choice.")

def run_program(): # Runs the program.
    while True:
        want = want_open() # prompt the user to choose weather to register or login or exit.
        if want == 0: # Admin.
            run_as_admin()
        elif want == 1:# register.
            take_user()
        elif want == 2: # login.
            run_as_user()
        elif want is None:# if the user choose to exit.
            return None
        else:
            print("Sorry, please enter a valid option from the list.")

def get_valid_acc_id(name):
    while True:
        user_input = input(f"Enter {name}'s account number(Q/q to exit): ")
        if check_exit(user_input) is None:
            return None
        try:
            account_id = int(user_input)
            if len(str(account_id)) == 5: # Convert the integer to string tp calc the length of the user, input it does
                return account_id         # not work directly on an integer.
            else:
                print("Sorry, the account id should be 5 numbers.")
        except ValueError:
            print("Sorry, please enter a valid number.")

def check_for_duplicate_friends(user, acc_id):
    found = False
    for friend in user.get_friends():  # checks for duplicate in acc number.
        if friend.get("acc_id") == acc_id:  # if the acc number already in the friends list
            found = True  # then found = true and exit the loop.
            return found
    else:
        return found

def show_transaction_history(user):
    print("<YOUR TRANSACTION HISTORY>")
    if len(user.get_transaction_history()) == 0:
        print("There's no messages.")
    else:
        print("You have " + str(len(user.get_transaction_history())) + " messages.")
        counter = 1
        for message in user.get_transaction_history():
            print(str(counter) + "-" + message)
            counter += 1

def add_friends(user):
    name = get_valid_name()
    if name is None:
        return None
    while True:
        acc_id = get_valid_acc_id(name)
        if acc_id is None:
            return None
        if not check_for_duplicate_friends(user, acc_id):
            user.set_friends(acc_id, name)
            break
        else:
            print("This friend is already in your friends list.")

def show_friends(user):
    print("<YOUR FRIENDS LIST>")
    if len(user.get_friends()) == 0:
        print("You have no friends.")
    else:
        print("You have " + str(len(user.get_friends())) + " friends.")
        counter = 1
        for friend in user.get_friends():
            print("#" + str(counter))
            print("Name: ", friend.get("name")) # prints the name of the current friend in the loop
            print("Account number: ", friend.get("acc_id")) # prints the acc number of the current friend in the loop
            counter +=1

def remove_friends(user):
    friends = user.get_friends()
    name = get_valid_name()
    if name is None:
        return

    found_friend = [] # a list to store the found users based on the name.
    for friend in friends:
        if friend.get("name") == name: # if the current user's name in the loop equal to the entered name by the input.
            found_friend.append(friend) # add the user to the new list.

    if not found_friend: # if there's no user found.
        print("Friend not found.")
        return
    if len(found_friend) == 1: # if there's only one friend? remove it directly.
        friends.remove(found_friend[0])
        print(f"Friend {name} has been removed successfully.")
        user.set_transaction_history(f"Friend {name} has been removed successfully.")

    else:
        print(f"Found multiple friends named \"{name}\":")
        counter = 1
        for friend in found_friend: # else if there's more than one user with the same name. Print the users.
            print(f"#{counter}")
            print("Name: ", friend.get("name"))
            print("Account number: ", friend.get("acc_id"))
            counter +=1

        while True:
            try:
                user_choice = input("Enter a number to delete (Q/q to exit): ")
                if check_exit(user_choice) is None:
                    return
                user_choice = int(user_choice)
                if user_choice in range(1, counter):
                    friends.remove(found_friend[user_choice - 1])
                    print(f"Friend {name} has been removed successfully.")
                    user.set_transaction_history(f"Friend {name} has been removed successfully.")
                    return
                else:
                    print("Sorry, please enter a number from the list.")
            except ValueError:
                print("Invalid input, please enter a number.")

def sittings (user, choice):
    sittings_options = {
                         1:lambda:user.display(),
                         2:lambda:edit_id(user),
                         3:lambda:edit_name(user),
                         4:lambda:edit_age(user), # Lambda is a short and temporarily function you can use it when you want a short task.
                         5:lambda:edit_username(user),
                         6:lambda:edit_password(user),
                         7:lambda:edit_acc_id(user)
                        }
    action = sittings_options.get(choice)
    action()

def edit_id(user):
    while True:
        new_id = get_valid_id()
        if new_id is None:
            return None
        if new_id == user.get_id():
            print("You can't enter the same ID.")
        else:
            update_id(new_id, user.get_id())
            user.set_id(new_id)
            user.set_transaction_history(f"ID has been changed to {new_id} successfully.")
            return

def update_id(new_id, uid):
    cur, ATM_db = get_cursor()
    try:
        cur.execute("UPDATE users SET id = ? WHERE id = ?", (new_id, uid))
    except sqlite3.IntegrityError: # To avoid the error of the integrity.
        print("Couldn't update the name.")
    ATM_db.commit()
    ATM_db.close()

def edit_name(user):
    while True:
        new_name = get_valid_name()
        if new_name is None:
            return None
        if new_name == user.get_name():
            print("You can't enter the same name.")
        else:
            update_name(new_name, user.get_id())
            user.set_name(new_name)
            user.set_transaction_history(f"Name has been changed to {new_name} successfully.")
            return

def update_name(new_name, uid):
    cur, ATM_db = get_cursor()
    try:
        cur.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, uid))
    except sqlite3.IntegrityError:
        print("Couldn't update the name.")
    ATM_db.commit()
    ATM_db.close()

def edit_age(user):
    while True:
        new_age = get_valid_age()
        if new_age is None:
            return None
        if new_age == user.get_age():
            print("You can't enter the same age.")
        else:
            update_age(new_age, user.get_id())
            user.set_age(new_age)
            user.set_transaction_history(f"Age has been changed to {new_age} successfully.")
            return

def update_age(new_age, uid):
    cur, ATM_db = get_cursor()
    try:
        cur.execute("UPDATE users SET age = ? WHERE id = ?", (new_age, uid))
    except sqlite3.IntegrityError:
        print("Couldn't update the name.")
    ATM_db.commit()
    ATM_db.close()

def edit_username(user):
    while True:
        new_username = get_valid_username()
        if new_username is None:
            return None
        if new_username == user.get_username():
            print("You can't enter the same username.")
        else:
            update_username(new_username, user.get_id())
            user.set_username(new_username)
            user.set_transaction_history(f"Username has been changed to {new_username} successfully.")
            return

def update_username(new_username, uid):
    cur, ATM_db = get_cursor()
    try:
        cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, uid))
    except sqlite3.IntegrityError:
        print("Couldn't update the name.")
    ATM_db.commit()
    ATM_db.close()

def edit_password(user):
    while True:
        new_pwd = get_strong_password(user.get_name())
        if new_pwd is None:
            return None
        if new_pwd == user.get_password():
            print("You can't enter the same password.")
        else:
            update_password(new_pwd, user.get_id())
            user.set_password(new_pwd)
            user.set_transaction_history(f"Password has been changed to {new_pwd} successfully.")
            return

def update_password(new_pwd, uid):
    cur, ATM_db = get_cursor()
    try:
        cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_pwd, uid))
    except sqlite3.IntegrityError:
        print("Couldn't update the name.")
    ATM_db.commit()
    ATM_db.close()

def edit_acc_id(user):
    while True:
        new_acc_id = get_valid_acc_id(user.get_name())
        if new_acc_id is None:
            return None
        if new_acc_id == user.get_acc_id():
            print("You can't enter the same account number.")
        else:
            update_acc_id(new_acc_id, user.get_id())
            user.set_acc_id(new_acc_id)
            user.set_transaction_history(f"Account number has been changed to {new_acc_id} successfully.")
            return

def update_acc_id(new_acc_id, uid):
    cur, ATM_db = get_cursor()
    try:
        cur.execute("UPDATE users SET acc_id = ? WHERE id = ?", (new_acc_id, uid))
    except sqlite3.IntegrityError:
        print("Couldn't update the name.")
    ATM_db.commit()
    ATM_db.close()

def show_profile(user):
    print(f"<{user.get_name()} profile>")
    user.display()

def take_id():
    while True:
        uid = input("Enter the ID (Q/q to exit): ")
        if check_exit(uid) is None:
            return None
        try:
            uid = int(uid)
            if check_user_already_added(uid):
                print("User found.")
                return uid
            else:
                print("User not found.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def admin_password(): # Check if the user is truly admin.
    admin_pwd = "whoami"
    pwd = input("Enter the admin password (Q/q to exit): ")
    if check_exit(pwd) is None:
        return None
    if pwd == admin_pwd:
        return True
    else:
        return False

def admin():
    # add_user(users_dict[admin]) # Admin is already inserted in the db.
    pwd = admin_password() # Let the admin enter the password.
    if pwd is None:
        return
    if pwd: # if the pwd is correct.
        cur, ATM_db = get_cursor()
        cur.execute("SELECT * FROM users WHERE id = 1")
        data = cur.fetchone()
        if data:
            aID, name, age, username, password, acc_id, balance = data
            return atm.ATM(aID, name, age, username, password, acc_id, balance)
    else:
        print("Administrator password incorrect.")

def run_as_admin():
    user = admin()
    if user is None:
        return
    print(f"\nAdmin {user.get_name()} logged in successfully.")
    user.display()
    take_choice(user)

def admin_sittings():
    options = {
        1:lambda:show_users(),
        2:lambda:edit_user(admin_enter_user_acc()),
        3:lambda:take_user(),
        4:lambda:delete_user(take_id())
    }
    while True:
        print("\n1-Show users.\n2-Edit user.\n3-Add user.\n4-Delete user.")
        choice = input("Enter a choice (Q/q to exit): ")

        if check_exit(choice) is None:
            return None
        else:
            try:
                action = options.get(int(choice))
                if action:
                    action()
                else:
                    print("Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def admin_enter_user_acc():
    uid = take_id() # Enter the user account by the ID.
    if uid is None:
        return None
    cur, ATM_db = get_cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (uid,))
    data = cur.fetchone()
    if data:
        uid, name, age, username, password, acc_id, balance = data
        return ATM(uid, name, age, username, password, acc_id, balance)
    else:
        print("User not found.")

def edit_user(user):
    if user is None:
        return None
    show_user(user.get_id())
    while True:
        print("\n1-Edit ID.\n2-Edit name.\n3-Edit Age.\n4-Edit username\n5-Edit password.\n6-Edit account number.")
        choice = input("Enter a choice (Q/q to exit): ")
        if check_exit(choice) is None:
            return None
        else:
            try:
                choice = int(choice)
                if choice in range (1,7):
                    sittings(user, choice+1)
                else:
                    print("Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def run_as_user():
    user = check_login()# prompt the user to enter he's username and password.

    if user is not None:  # if the user continues.
        print(f"\nUser logged in successfully.")
        user.display()
        take_choice(user)
    else:  # if the user choose to before loges in quit.
        print("Cannot login.")

def user_sittings(user):
    while True:
        choice = input("\n1-Show profile.\n2-Edit ID.\n3-Edit name.\n4-Edit age.\n5-Edit username."
                              "\n6-Edit password.\n7-Edit account number.\n\n(Q/q)-Exit.\n")

        if check_exit(choice) is None:
            return None
        else:
            try:
                choice = int(choice)
                if choice in range(1,8):
                    sittings(user, choice)
                else:
                    print("Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def check_user_already_added(uid):
    cur,ATM_db = get_cursor()
    cur = ATM_db.cursor()
    cur.execute("SELECT id FROM users WHERE id = ?", (uid,))
    data = cur.fetchone()
    ATM_db.commit()
    ATM_db.close()
    if data:
        return not None

def show_users():
    with connect() as ATM_db:
        cur = ATM_db.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        counter = 1
        for row in data:
            print(f"\nUser #{counter}:")
            print("ID:", row[0])
            print("Name:", row[1])
            print("Age:", row[2])
            print("Username:", row[3])
            print("Password:", row[4])
            print("Account number:", row[5])
            counter += 1
    ATM_db.commit()

def search_friends(user):
    while True:
        if len(user.get_friends()) == 0:
            print("You have no friends")
            return

        found_friends = [] # A list to store the friends who have the searched name.

        print("Search by name.")
        friend_name = get_valid_name()
        if friend_name is None:
            return None

        for friend in user.get_friends(): # A loop to move throw the dicts of friends in the list friends of the object.
            if friend.get("name") == friend_name: # if the current dict has the same name of the input.
                found_friends.append(friend) # add the dict of the friend to the new list here.

        if len(found_friends) == 0:
            print("There's no friend with this name.")

        else:
            for friend in found_friends: # Print the friends.
                print("Name:", friend.get("name"))
                print("Account number:", friend.get("acc_id"))

        found_friends.clear() #Clears the whole list.
        repeat = input("You wanna search for another name?(y|n)")
        if repeat.lower() == 'n': #if the user choose not to search for another one. Else the function will continue.
            return #Exit the function.

# create_table() # table is already created.
users_dict = {}  # a dict to store lists of users.

while True: # run the program.
    if run_program() is None: #Stop the running.
        break

print("\nThank you for using our bank.\nWe hope to see you soon.")
