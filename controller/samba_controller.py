import os
import subprocess
import random
import string

class SambaManager:
    """
    Gère la gestion des utilisateurs et des partages Samba.

    Args:
        smb_conf_path (str): Chemin du fichier de configuration smb.conf. Par défaut, '/etc/samba/smb.conf'.
        fixed_share_path (str): Chemin du répertoire de partage fixe. Par défaut, '/srv/samba/fixedshare'.

    Attributes:
        smb_conf_path (str): Chemin du fichier de configuration smb.conf.
        fixed_share_path (str): Chemin du répertoire de partage fixe.
    Methods:
        generate_random_username(self, length=8): Génère un nom d'utilisateur aléatoire.
        add_user(self, username, password): Ajoute un utilisateur au système et à Samba.
        delete_user(self, username): Supprime un utilisateur de Samba et du système.
        create_share(self, share_name, username): Crée un partage Samba avec le nom spécifié et l'attribue à l'utilisateur spécifié.
        remove_share(self, share_name): Supprime un partage Samba.
        start_samba(self): Démarre les services Samba (smbd et nmbd).
        stop_samba(self): Arrête les services Samba (smbd et nmbd).
        create_random_user_and_share(self, share_name): Crée un utilisateur aléatoire et un partage associé.
        remove_random_user_and_share(self, share_name, username): Supprime un utilisateur et le partage associé.
        open_share(self): Démarre les services Samba pour ouvrir le partage.
        close_share(self): Arrête les services Samba pour fermer le partage.
    """

    def __init__(self, smb_conf_path='/etc/samba/smb.conf', fixed_share_path='/srv/samba/fixedshare'):
        self.smb_conf_path = smb_conf_path
        self.fixed_share_path = fixed_share_path

    def generate_random_username(self, length=8):
        """
        Génère un nom d'utilisateur aléatoire.

        Args:
            length (int): Longueur du nom d'utilisateur généré. Par défaut, 8.

        Returns:
            str: Nom d'utilisateur aléatoire.

        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def add_user(self, username, password):
        """
        Ajoute un utilisateur au système et à Samba.

        Args:
            username (str): Nom d'utilisateur.
            password (str): Mot de passe de l'utilisateur.

        """
        # Ajoute l'utilisateur au système
        subprocess.run(['sudo', 'useradd', '-m', username], check=True)
        # Définit le mot de passe de l'utilisateur
        subprocess.run(['sudo', 'chpasswd'], input=f'{username}:{password}', text=True, check=True)
        # Ajoute l'utilisateur à Samba
        subprocess.run(['sudo', 'smbpasswd', '-a', username], input=f'{password}\n{password}', text=True, check=True)

    def delete_user(self, username):
        """
        Supprime un utilisateur de Samba et du système.

        Args:
            username (str): Nom d'utilisateur.

        """
        # Supprime l'utilisateur de Samba
        subprocess.run(['sudo', 'smbpasswd', '-x', username], check=True)
        # Supprime l'utilisateur du système
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)

    def create_share(self, share_name, username):
        """
        Crée un partage Samba avec le nom spécifié et l'attribue à l'utilisateur spécifié.

        Args:
            share_name (str): Nom du partage.
            username (str): Nom d'utilisateur auquel attribuer le partage.

        """
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
        # Vérifie que le répertoire de partage existe
        os.makedirs(self.fixed_share_path, exist_ok=True)
        subprocess.run(['sudo', 'chown', '-R', f'{username}:{username}', self.fixed_share_path], check=True)
        subprocess.run(['sudo', 'chmod', '-R', '0777', self.fixed_share_path], check=True)

        # Ajoute le partage au fichier smb.conf
        with open(self.smb_conf_path, 'a') as smb_conf:
            smb_conf.write(share_config)

    def remove_share(self, share_name):
        """
        Supprime un partage Samba.

        Args:
            share_name (str): Nom du partage à supprimer.

        """
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
        """
        Démarre les services Samba (smbd et nmbd).

        """
        subprocess.run(['sudo', 'systemctl', 'start', 'smbd'], check=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'nmbd'], check=True)

    def stop_samba(self):
        """
        Arrête les services Samba (smbd et nmbd).

        """
        subprocess.run(['sudo', 'systemctl', 'stop', 'smbd'], check=True)
        subprocess.run(['sudo', 'systemctl', 'stop', 'nmbd'], check=True)

    def create_random_user_and_share(self, share_name):
        """
        Crée un utilisateur aléatoire et un partage associé.

        Args:
            share_name (str): Nom du partage.

        Returns:
            tuple: Nom d'utilisateur et mot de passe générés.

        """
        username = self.generate_random_username()
        password = self.generate_random_username(12)  # Génère un mot de passe aléatoire de longueur 12
        self.add_user(username, password)
        self.create_share(share_name, username)
        return username, password

    def remove_random_user_and_share(self, share_name, username):
        """
        Supprime un utilisateur et le partage associé.

        Args:
            share_name (str): Nom du partage.
            username (str): Nom d'utilisateur.

        """
        self.remove_share(share_name)
        self.delete_user(username)

    def open_share(self):
        """
        Démarre les services Samba pour ouvrir le partage.

        """
        self.start_samba()

    def close_share(self):
        """
        Arrête les services Samba pour fermer le partage.

        """
        self.stop_samba()


