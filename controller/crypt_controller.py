import os
from cryptography.fernet import Fernet

class FolderEncryptor:
    """
    Une classe qui fournit des méthodes pour crypter et décrypter des fichiers et des dossiers.

    Args:
        key (bytes): L'empreinte utilisée pour le cryptage et le décryptage.

    Attributs:
        key (bytes): L'empreinte utilisée pour le cryptage et le décryptage.
    """

    def __init__(self, key):
        self.key = key

    def encrypt_file(self, file_path):
        """
        Crypte un fichier en utilisant la clé de cryptage fournie.

        Args:
            file_path (str): Le chemin vers le fichier à crypter.
        """
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = self._encrypt_data(data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, file_path):
        """
        Décrypte un fichier en utilisant la clé de cryptage fournie.

        Args:
            file_path (str): Le chemin vers le fichier à décrypter.
        """
        with open(file_path, 'rb') as file:
            data = file.read()
        decrypted_data = self._decrypt_data(data)
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)

    def encrypt_folder(self, folder_path):
        """
        Crypte tous les fichiers dans un dossier et ses sous-dossiers en utilisant la clé de cryptage fournie.

        Args:
            folder_path (str): Le chemin vers le dossier à crypter.
        """
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.encrypt_file(file_path)

    def decrypt_folder(self, folder_path):
        """
        Décrypte tous les fichiers dans un dossier et ses sous-dossiers en utilisant la clé de cryptage fournie.

        Args:
            folder_path (str): Le chemin vers le dossier à décrypter.
        """
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.decrypt_file(file_path)

    def _encrypt_data(self, data):
        """
        Crypte les données fournies en utilisant la clé de cryptage.

        Args:
            data (bytes): Les données à crypter.

        Returns:
            bytes: Les données cryptées.
        """
        cipher = Fernet(self.key)
        return cipher.encrypt(data)

    def _decrypt_data(self, data):
        """
        Décrypte les données fournies en utilisant la clé de cryptage.

        Args:
            data (bytes): Les données à décrypter.

        Returns:
            bytes: Les données décryptées.
        """
        cipher = Fernet(self.key)
        return cipher.decrypt(data)
