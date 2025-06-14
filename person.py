class Person:
    def __init__(self, uid, name, age):
        self.__userID = uid
        self.__name = name
        self.__age = age
    def set_name(self, name):
        self.__name = name
        print(f"Name has been changed to {name} successfully.")
    def set_age(self, age):
        self.__age = age
        print(f"Age has been changed to {age} successfully.")
    def set_id(self,user_id):
        self.__userID = user_id
        print(f"ID has been changed to {user_id} successfully.")
    def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def get_id(self):
        return self.__userID
    def display(self):
        print("ID:", self.__userID)
        print('Name:', self.__name)
        print('Age:', self.__age)