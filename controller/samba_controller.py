import os
import subprocess
import random
import string

class SambaManager:
    def __init__(self, smb_conf_path='/etc/samba/smb.conf', fixed_share_path='/srv/samba/fixedshare'):
        self.smb_conf_path = smb_conf_path
        self.fixed_share_path = fixed_share_path

    def generate_random_username(self, length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def add_user(self, username, password):
        # Add the user to the system
        subprocess.run(['sudo', 'useradd', '-m', username], check=True)
        # Set the user's password
        subprocess.run(['sudo', 'chpasswd'], input=f'{username}:{password}', text=True, check=True)
        # Add the user to Samba
        subprocess.run(['sudo', 'smbpasswd', '-a', username], input=f'{password}\n{password}', text=True, check=True)

    def delete_user(self, username):
        # Delete the user from Samba
        subprocess.run(['sudo', 'smbpasswd', '-x', username], check=True)
        # Delete the user from the system
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)

    def create_share(self, share_name, username):
        share_config = f"""
[{share_name}]
   path = {self.fixed_share_path}
   browseable = yes
   writable = yes
   valid users = {username}
   create mask = 0777
   directory mask = 0777
   force user = {username}
   force group = {username}
"""
        # Ensure the share directory exists
        os.makedirs(self.fixed_share_path, exist_ok=True)
        subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', self.fixed_share_path], check=True)
        subprocess.run(['sudo', 'chmod', '-R', '0777', self.fixed_share_path], check=True)

        # Add the share to the smb.conf file
        with open(self.smb_conf_path, 'a') as smb_conf:
            smb_conf.write(share_config)

    def remove_share(self, share_name):
        with open(self.smb_conf_path, 'r') as smb_conf:
            lines = smb_conf.readlines()

        with open(self.smb_conf_path, 'w') as smb_conf:
            inside_share = False
            for line in lines:
                if line.strip().startswith(f'[{share_name}]'):
                    inside_share = True
                elif inside_share and line.strip().startswith('['):
                    inside_share = False

                if not inside_share:
                    smb_conf.write(line)

    def start_samba(self):
        subprocess.run(['sudo', 'systemctl', 'start', 'smbd'], check=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'nmbd'], check=True)

    def stop_samba(self):
        subprocess.run(['sudo', 'systemctl', 'stop', 'smbd'], check=True)
        subprocess.run(['sudo', 'systemctl', 'stop', 'nmbd'], check=True)

    def create_random_user_and_share(self, share_name):
        username = self.generate_random_username()
        password = self.generate_random_username(12)  # Generating a random password of length 12
        self.add_user(username, password)
        self.create_share(share_name, username)
        return username, password

    def open_share(self):
        self.start_samba()

    def close_share(self):
        self.stop_samba()


