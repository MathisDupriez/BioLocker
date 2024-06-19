import hashlib


class PasswordOperations:
    """
    Classe utilitaire pour les opérations liées aux mots de passe.

    Attributes:
        Aucun attribut.

    Methods:
        verify_password_strength(password):
            Vérifie la force d'un mot de passe.

        hash_password(password):
            Hache le mot de passe en utilisant l'algorithme SHA256.

        verify_password(password, hashed_password):
            Vérifie si le mot de passe correspond au hachage.
    """
    
    @staticmethod
    def verify_password_strength(password):
        """
        Vérifie la force d'un mot de passe.

        Args:
            password (str): Le mot de passe à vérifier.

        Returns:
            bool: True si le mot de passe est suffisamment fort, False sinon.
        """
        return len(password) >= 8

    @staticmethod
    def hash_password(password):
        """
        Hache le mot de passe en utilisant l'algorithme SHA256.

        Args:
            password (str): Le mot de passe à hacher.

        Returns:
            str: Le mot de passe haché.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    @staticmethod
    def verify_password(password, hashed_password):
        """
        Vérifie si le mot de passe correspond au hachage.

        Args:
            password (str): Le mot de passe à vérifier.
            hashed_password (str): Le mot de passe haché.

        Returns:
            bool: True si le mot de passe correspond au hachage, False sinon.
        """
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password