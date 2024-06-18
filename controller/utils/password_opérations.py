import hashlib


class PasswordOperations:

    @staticmethod
    def verify_password_strength(password):
        # Vérifie la force d'un mot de passe
        # Exemple de critères de force : longueur minimale, présence de lettres majuscules, minuscules, chiffres, caractères spéciaux, etc.
        # Implémentez vos propres critères de force ici
        return len(password) >= 8

    @staticmethod
    def hash_password(password):
        # Hache le mot de passe en utilisant l'algorithme SHA256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    @staticmethod
    def verify_password(password, hashed_password):
        # Vérifie si le mot de passe correspond au hachage
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password