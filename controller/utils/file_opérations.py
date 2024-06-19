import hashlib
import base64
from controller.crypt_controller import FolderEncryptor

class FileOperations:
    """
    Classe qui représente les opérations de fichiers.

    Cette classe permet de chiffrer et déchiffrer des dossiers en utilisant l'empreinte digitale comme clé d'encryption.
    
    Attributes:
        view_ops: Vue principale de l'application.
        controller: Contrôleur de l'empreinte digitale.
    
    Methods:
        encrypt_folder(folder_path): Encrypte un dossier en utilisant l'empreinte digitale.
        decrypt_folder(folder_path): Décrypte un dossier en utilisant l'empreinte digitale.
        _perform_folder_encryption(folder_path): Effectue le chiffrement du dossier en utilisant une clé générée à partir de l'empreinte digitale.
        _perform_folder_decryption(folder_path): Effectue le déchiffrement du dossier en utilisant une clé générée à partir de l'empreinte digitale.
        _generate_encryption_key(): Génère une clé d'encryption à partir de l'empreinte digitale.
    
    """

    def __init__(self, view_ops, controller):
        self.view_ops = view_ops
        self.controller = controller

    def encrypt_folder(self,folder_path):
        """
        Encrypte un dossier en utilisant l'empreinte digitale.

        :param folder_path: Chemin du dossier à encrypter.
        :type folder_path: str
        """
        self._perform_folder_encryption(folder_path)

    def decrypt_folder(self,folder_path):
        """
        Décrypte un dossier en utilisant l'empreinte digitale.

        :param folder_path: Chemin du dossier à décrypter.
        :type folder_path: str
        """
        self._perform_folder_decryption(folder_path)

    def _perform_folder_encryption(self,folder_path):
        """
        Effectue le chiffrement du dossier en utilisant une clé générée à partir de l'empreinte digitale.

        :param folder_path: Chemin du dossier à encrypter.
        :type folder_path: str
        """
        key = self._generate_encryption_key()
        encryptor = FolderEncryptor(key)
        encryptor.encrypt_folder(folder_path)

    def _perform_folder_decryption(self, folder_path):
        """
        Effectue le déchiffrement du dossier en utilisant une clé générée à partir de l'empreinte digitale.

        :param folder_path: Chemin du dossier à décrypter.
        :type folder_path: str
        """
        key = self._generate_encryption_key()
        encryptor = FolderEncryptor(key)
        encryptor.decrypt_folder(folder_path)

    def _generate_encryption_key(self):
        """
        Génère une clé d'encryption à partir de l'empreinte digitale.

        :return: Clé d'encryption générée.
        :rtype: bytes
        """
        empreinte_hex = self.controller.Finger_print
        empreinte_bytes = bytes.fromhex(empreinte_hex)
        hachage = hashlib.sha256(empreinte_bytes).digest()
        return base64.urlsafe_b64encode(hachage)
