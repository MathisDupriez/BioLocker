import json

class PasswordReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_password(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            # Expected JSON structure:
            # {
            #     "users": [
            #         {
            #             "username": "user1",
            #             "password": "password1"
            #         },
            #         {
            #             "username": "user2",
            #             "password": "password2"
            #         },
            #         ...
            #     ]
            # }
            for user in data['users']:
                if 'password' in user:
                    password = user['password']
                    return password
            return None

    def get_password_for_user(self, username):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            print(data)
            for user in data['users']:
                if 'username' in user and user['username'] == username:
                    if 'password' in user:
                        password = user['password']
                        return password
            return None
