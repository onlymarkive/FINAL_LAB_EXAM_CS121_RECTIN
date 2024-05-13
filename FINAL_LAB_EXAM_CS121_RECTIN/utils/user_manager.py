import os
from .user import User

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/users.txt"):
            with open("data/users.txt", "w") as file:
                pass
        else:
            with open("data/users.txt", "r") as file:
                for line in file:
                    username, password = line.strip().split(",")
                    self.users[username] = User(username,password)

    def save_users(self):
        with open("data/users.txt", "a") as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password}\n")

    def validate_username(self, username):
        if len(username) < 4:
            print("Username must be at least 4 characters long.")
            return False
        return True
    
    def validate_password(self, password):
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        return True
    
    def register(self, username, password):
        if self.validate_username(username) and self.validate_password(password):
            if username not in self.users:
                new_user = User(username, password)
                self.users[username] = new_user
                self.save_users()
                print("Registration successful.")
            else:
                print("Username already exists.")
        else:
            print("Invalid username or password.")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            print("Login successful.")
            return self.users[username]
        else:
            print("Invalid username or password.")
            return None