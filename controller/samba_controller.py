import subprocess

class SambaController:
    def __init__(self):
        print("Samba Controller initialized")

    def start_server(self):
        subprocess.run(["sudo", "systemctl", "start", "smbd"])

    def stop_server(self):
        subprocess.run(["sudo", "systemctl", "stop", "smbd"])

    def restart_server(self):
        subprocess.run(["sudo", "systemctl", "restart", "smbd"])

    def add_user(self, username, password):
        subprocess.run(["sudo", "smbpasswd", "-a", username], input=password.encode())

    def remove_user(self, username):
        subprocess.run(["sudo", "smbpasswd", "-x", username])

    def list_users(self):
        subprocess.run(["pdbedit", "-L"])

    def share_directory(self, directory_path, share_name):
        subprocess.run(["sudo", "net", "usershare", "add", share_name, directory_path, "-U", self.username])

    def unshare_directory(self, share_name):
        subprocess.run(["sudo", "net", "usershare", "delete", share_name])
