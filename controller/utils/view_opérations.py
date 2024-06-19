from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

class ViewOperations:
    """
    Classe représentant les opérations de vue.

    Cette classe gère les opérations de journalisation et d'affichage de messages dans l'interface utilisateur.

    Attributes:
        view (object): L'objet de la vue.
        controller (object): L'objet du contrôleur.
    Methods:
        __init__(self, view, controller): Initialise une nouvelle instance de la classe ViewOperations.
        log(self, message, log_type="info"): Ajoute un message de journalisation à l'interface utilisateur.
        log_fingerprint_start(self): Journalise le début de la procédure de déverrouillage par empreinte digitale.
        log_finger_time_remaining(self, time_remaining): Journalise le temps restant pour placer le doigt sur le capteur.
        log_fingerprint_not_detected(self): Journalise l'absence de détection d'empreinte digitale sur le capteur.
        log_enter_code_message(self): Journalise le message demandant à l'utilisateur d'entrer son code.
        log_code_entered(self, code): Journalise la saisie du code par l'utilisateur.
        log_code_correct(self): Journalise la confirmation que le code saisi est correct.
        log_code_incorrect(self): Journalise l'erreur de saisie du code.
        log_ip_address(self, ip_address): Journalise l'adresse IP de l'appareil.
        log_folder_action(self, action): Journalise l'action en cours sur le dossier.
        log_decrypting_done(self): Journalise la fin du décryptage du dossier.
        log_encrypting_done(self): Journalise la fin du cryptage du dossier.
        log_handle_fingerprint_match(self): Journalise la correspondance d'empreinte digitale trouvée.
        log_handle_fingerprint_mismatch(self): Journalise l'absence de correspondance d'empreinte digitale.
        log_samba_start(self): Journalise le démarrage du serveur Samba.
        log_samba_stop(self): Journalise l'arrêt du serveur Samba.
        log_samba_share_created(self, share_name, username, password): Journalise la création d'un partage Samba.
        log_samba_share_already_open(self, share_name, username, password): Journalise l'erreur de tentative d'ouverture d'un partage Samba déjà ouvert.
        log_you_cant_open(self): Journalise l'erreur de tentative d'ouverture d'un partage Samba lorsque le dossier est crypté.
        log_decryption_already_done(self): Journalise l'erreur de tentative de décryptage d'un dossier déjà décrypté.
        log_encryption_already_done(self): Journalise l'erreur de tentative de cryptage d'un dossier déjà crypté.
    """

    def __init__(self, view, controller):
        """
        Initialise une nouvelle instance de la classe ViewOperations.

        Args:
            view (object): L'objet de la vue.
            controller (object): L'objet du contrôleur.
        """
        self.controller = controller
        self.view = view
        self.log_start_app()

    def log(self, message, log_type="info"):
        """
        Ajoute un message de journalisation à l'interface utilisateur.

        Args:
            message (str): Le message à ajouter.
            log_type (str, optional): Le type de journalisation. Par défaut, "info".
        """
        self.view.add_log(message, log_type)

    def log_fingerprint_start(self):
        """
        Journalise le début de la procédure de déverrouillage par empreinte digitale.
        """
        self.log("Procédure de déverrouillage lancée.")
        self.log("Début de la vérification de l'empreinte digitale.")
        self.log("Veuillez placer votre doigt sur le capteur et le maintenir jusqu'à l'extinction de la lumière.", "instruction")

    def log_finger_time_remaining(self, time_remaining):
        """
        Journalise le temps restant pour placer le doigt sur le capteur.

        Args:
            time_remaining (int): Le temps restant en secondes.
        """
        self.log(f"Temps restant pour placer votre doigt : {time_remaining} secondes.")

    def log_fingerprint_not_detected(self):
        """
        Journalise l'absence de détection d'empreinte digitale sur le capteur.
        """
        self.log("Aucun doigt détecté sur le capteur. Déverrouillage annulé.", "error")

    def log_enter_code_message(self):
        """
        Journalise le message demandant à l'utilisateur d'entrer son code.
        """
        self.log("Veuillez entrer votre code. Appuyez sur 'ok' pour valider. Appuyez sur 'C' pour effacer.", "instruction")

    def log_code_entered(self, code):
        """
        Journalise la saisie du code par l'utilisateur.

        Args:
            code (str): Le code saisi.
        """
        self.log(f"Code saisi.", "success")

    def log_code_correct(self):
        """
        Journalise la confirmation que le code saisi est correct.
        """
        self.log("Code correct.", "success")
        self.log("Début de dévérouillage.", "info")

    def log_code_incorrect(self):
        """
        Journalise l'erreur de saisie du code.
        """
        self.log("Code incorrect. Veuillez réessayer.", "error")

    def log_ip_address(self, ip_address):
        """
        Journalise l'adresse IP de l'appareil.

        Args:
            ip_address (str): L'adresse IP de l'appareil.
        """
        self.log(f"Adresse IP de l'appareil : {ip_address}")

    def log_folder_action(self, action):
        """
        Journalise l'action en cours sur le dossier.

        Args:
            action (str): L'action en cours sur le dossier.
        """
        self.log(f"{action.capitalize()} du dossier en cours...")

    def log_decrypting_done(self):
        """
        Journalise la fin du décryptage du dossier.
        """
        self.log("Dossier décrypté avec succès.", "success")

    def log_encrypting_done(self):
        """
        Journalise la fin du cryptage du dossier.
        """
        self.log("Dossier crypté avec succès.", "success")

    def log_handle_fingerprint_match(self):
        """
        Journalise la correspondance d'empreinte digitale trouvée.
        """
        self.log("Correspondance d'empreinte trouvée.", "success")

    def log_handle_fingerprint_mismatch(self):
        """
        Journalise l'absence de correspondance d'empreinte digitale.
        """
        self.log("Aucune correspondance d'empreinte trouvée.", "error")
        self.log("Procédure avortée.", "error")

    def log_samba_start(self):
        """
        Journalise le démarrage du serveur Samba.
        """
        self.log("Démarrage du serveur Samba en cours...")
        self.log("Serveur Samba démarré.", "success")

    def log_samba_stop(self):
        """
        Journalise l'arrêt du serveur Samba.
        """
        self.log("Arrêt du serveur Samba en cours...")
        self.log("Serveur Samba arrêté.", "success")

    def log_samba_share_created(self, share_name, username, password):
        """
        Journalise la création d'un partage Samba.

        Args:
            share_name (str): Le nom du partage.
            username (str): Le nom d'utilisateur.
            password (str): Le mot de passe.
        """
        self.log(f"Nom du partage : {share_name}", "instruction")
        self.log(f"Nom d'utilisateur : {username}", "instruction")
        self.log(f"Mot de passe : {password}", "instruction")
        ip = self.controller.get_local_ip()
        self.log(f"Url SMB : \\\\{ip}", "instruction")

    def log_samba_share_already_open(self, share_name, username, password):
        """
        Journalise l'erreur de tentative d'ouverture d'un partage Samba déjà ouvert.

        Args:
            share_name (str): Le nom du partage.
            username (str): Le nom d'utilisateur.
            password (str): Le mot de passe.
        """
        self.log(f"Le partage Samba {share_name} est déjà ouvert.", "error")
        self.log(f"Nom d'utilisateur : {username}")
        self.log(f"Mot de passe : {password}")

    def log_you_cant_open(self):
        """
        Journalise l'erreur de tentative d'ouverture d'un partage Samba lorsque le dossier est crypté.
        """
        self.log("Vous ne pouvez pas ouvrir un partage Samba si le dossier est crypté.", "error")

    def log_decryption_already_done(self):
        """
        Journalise l'erreur de tentative de décryptage d'un dossier déjà décrypté.
        """
        self.log("Le dossier est déjà décrypté.", "error")

    def log_encryption_already_done(self):
        """
        Journalise l'erreur de tentative de cryptage d'un dossier déjà crypté.
        """
        self.log("Le dossier est déjà crypté.", "error")

    def log_samba_share_already_closed(self):
        """
        Journalise l'erreur de tentative de fermeture d'un partage Samba déjà fermé.
        """
        self.log("Aucun partage Samba ouvert.", "error")

    def log_closing_sharing_for_encryption(self):
        """
        Journalise la fermeture du partage Samba pour la gestion du cryptage.
        """
        self.log("Fermeture du partage Samba pour la gestion du cryptage.", "info")

    def show_file_chooser(self, action):
        """
        Affiche le sélecteur de fichiers pour l'action donnée.

        Args:
            action (str): L'action pour laquelle afficher le sélecteur de fichiers.
        """
        chooser = FileChooserListView()
        popup = Popup(title=f"Choisir un fichier à {action}", content=chooser)
        popup.open()

    def log_start_app(self):
        """
        Journalise le démarrage de l'application.
        """
        self.log("Démarrage de l'application, veillez sur les points suivants :", "info")
        self.log("- Assurez-vous que le niveau de batterie est suffisant.", "error")
        self.log("- Ne forcez jamais l'arrêt du système en ayant un coffre-fort décrypté.", "error")
        self.log("- Assurez-vous de la connexion internet.", "error")

        # Log successful startup
        self.log("Application démarrée avec succès.", "success")

        
