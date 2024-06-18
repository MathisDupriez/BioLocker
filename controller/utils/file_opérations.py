import hashlib
import base64
from controller.crypt_controller import FolderEncryptor

class FileOperations:
    def __init__(self, view_ops, controller):
        self.view_ops = view_ops
        self.controller = controller

    def encrypt_folder(self):
        """
        Encrypt a folder using the fingerprint.
        """
        self.view_ops.log_folder_action("Encrypting", "Folder encrypted successfully.")
        self._perform_folder_encryption('/home/mathis/project/testencrypt')

    def decrypt_folder(self):
        """
        Decrypt a folder using the fingerprint.
        """
        self.view_ops.log_folder_action("Decrypting", "Folder decrypted successfully.")
        self._perform_folder_decryption('/home/mathis/project/testencrypt')

    def _perform_folder_encryption(self, folder_path):
        key = self._generate_encryption_key()
        encryptor = FolderEncryptor(key)
        encryptor.encrypt_folder(folder_path)

    def _perform_folder_decryption(self, folder_path):
        key = self._generate_encryption_key()
        encryptor = FolderEncryptor(key)
        encryptor.decrypt_folder(folder_path)

    def _generate_encryption_key(self):
        empreinte_hex = self.controller.Finger_print
        empreinte_bytes = bytes.fromhex(empreinte_hex)
        hachage = hashlib.sha256(empreinte_bytes).digest()
        return base64.urlsafe_b64encode(hachage)
