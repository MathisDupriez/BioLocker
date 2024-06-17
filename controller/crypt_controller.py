import os
from cryptography.fernet import Fernet

class FolderEncryptor:
    """
    A class that provides methods to encrypt and decrypt files and folders.

    Args:
        key (bytes): The encryption key used for encryption and decryption.

    Attributes:
        key (bytes): The encryption key used for encryption and decryption.
    """

    def __init__(self, key):
        self.key = key

    def encrypt_file(self, file_path):
        """
        Encrypts a file using the provided encryption key.

        Args:
            file_path (str): The path to the file to be encrypted.
        """
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = self._encrypt_data(data)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, file_path):
        """
        Decrypts a file using the provided encryption key.

        Args:
            file_path (str): The path to the file to be decrypted.
        """
        with open(file_path, 'rb') as file:
            data = file.read()
        decrypted_data = self._decrypt_data(data)
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)

    def encrypt_folder(self, folder_path):
        """
        Encrypts all files in a folder and its subfolders using the provided encryption key.

        Args:
            folder_path (str): The path to the folder to be encrypted.
        """
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.encrypt_file(file_path)

    def decrypt_folder(self, folder_path):
        """
        Decrypts all files in a folder and its subfolders using the provided encryption key.

        Args:
            folder_path (str): The path to the folder to be decrypted.
        """
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.decrypt_file(file_path)

    def _encrypt_data(self, data):
        """
        Encrypts the provided data using the encryption key.

        Args:
            data (bytes): The data to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        cipher = Fernet(self.key)
        return cipher.encrypt(data)

    def _decrypt_data(self, data):
        """
        Decrypts the provided data using the encryption key.

        Args:
            data (bytes): The data to be decrypted.

        Returns:
            bytes: The decrypted data.
        """
        cipher = Fernet(self.key)
        return cipher.decrypt(data)
