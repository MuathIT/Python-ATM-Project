import person

class Account(person.Person):
    def __init__(self, uid, name, age, username, password):
        super().__init__(uid,name,age)
        self.__username = username
        self.__password = password
    def set_username(self, username):
        self.__username = username
        print(f"Username has been changed to {username} successfully")
    def set_password(self, password):
        self.__password = password
        print(f"Password has been changed to {password} successfully.")
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def display(self):
        super().display()
        print('Username:', self.__username)