from kivy.clock import Clock
from controller.samba_controller import SambaManager
from controller.utils.fingerprint_action import FingerprintActions
from model.password_model import PasswordReader
import socket
import atexit
import random

from controller.utils.file_opérations import FileOperations
from controller.utils.view_opérations import ViewOperations
from controller.utils.password_opérations import PasswordOperations


class FingerprintController:
    """
    Contrôleur pour l'authentification par empreinte digitale.

    Attributes:
        model (object): L'objet modèle utilisé pour l'authentification par empreinte digitale.
        view (object): L'objet vue utilisé pour l'affichage.
        samba_manager (object): L'objet gestionnaire Samba utilisé pour le partage de fichiers.
        fingerprint_done (bool): Indique si l'authentification par empreinte digitale est terminée.
        code_entered (str): Le code saisi par l'utilisateur.
        Finger_print (str): L'empreinte digitale de l'utilisateur.
        checking_Code (bool): Indique si le code est en cours de vérification.
        locking (bool): Indique si le système est verrouillé.
        unlocking (bool): Indique si le système est déverrouillé.
        encryption_state (bool): Indique l'état du chiffrement des fichiers.
        sharing_state (bool): Indique l'état du partage de fichiers.
        current_username (str): Le nom d'utilisateur actuel.
        current_password (str): Le mot de passe actuel.
        share_name (str): Le nom du partage Samba.
        username_share (str): Le nom d'utilisateur pour le partage Samba.
        password_share (str): Le mot de passe pour le partage Samba.
        view_ops (object): L'objet opérations de vue.
        actions (object): L'objet actions d'authentification par empreinte digitale.
        file_ops (object): L'objet opérations de fichiers.
        password_reader (object): L'objet lecteur de mots de passe.

    Methods:
        unlock(instance): Déverrouille le système en utilisant l'authentification par empreinte digitale.
        lock(instance): Verrouille le système.
        wait_for_fingerprint(dt): Attend que l'authentification par empreinte digitale soit terminée.
        identify_fingerprint(): Identifie l'empreinte digitale et effectue les actions nécessaires.
        check_code(): Vérifie le code saisi par l'utilisateur.
        verify_code(): Vérifie le code saisi.
        handle_crypt(): Gère le chiffrement et le déchiffrement des fichiers.
        start_samba(): Démarre le partage Samba.
        stop_samba(): Arrête le partage Samba.
        numpad_button_pressed(instance): Gère les événements de pression des boutons du pavé numérique.
        get_local_ip(): Récupère l'adresse IP locale de l'appareil.
        ip_button_pressed(): Gère l'événement de pression du bouton IP.
        exit_handler(): Fonction exécutée à la sortie du programme.
        select_file_encrypt(): Sélectionne un fichier pour le chiffrement.
        select_file_decrypt(): Sélectionne un fichier pour le déchiffrement.
    """

    def __init__(self, model, view, samba_manager):
        """
        Initialise le contrôleur avec le modèle, la vue et le gestionnaire Samba.

        Args:
            model (object): L'objet modèle utilisé par le contrôleur.
            view (object): L'objet vue utilisé par le contrôleur.
            samba_manager (object): L'objet gestionnaire Samba utilisé par le contrôleur.

        """
        self.model = model
        self.view = view
        self.samba_manager = samba_manager
        
        self.fingerprint_done = False
        self.code_entered = ""
        self.Finger_print = None
        self.checking_Code = False
        self.locking = False
        self.unlocking = False

        self.encryption_state = True
        self.sharing_state = False

        self.current_username = None
        self.current_password = None

        self.share_name = None
        self.username_share = None
        self.password_share = None

        self.view_ops = ViewOperations(view, self)
        self.actions = FingerprintActions(model, self.view_ops, self)
        self.file_ops = FileOperations(self.view_ops, self)
        self.password_reader = PasswordReader('/home/mathis/project/micro-system2024b2q2-main/model/userDb.json')
        
        atexit.register(self.exit_handler)

    def unlock(self, instance):
        """
        Déverrouille le système en utilisant l'authentification par empreinte digitale.
        
        Args:
            instance (object): L'instance de l'objet qui a déclenché l'événement.
        """
        self.unlocking = True
        self.actions.check_fingerprint(instance)
        Clock.schedule_interval(self.wait_for_fingerprint, 0.1)

    def lock(self, instance):
        """
        Verrouille le système.
        
        Args:
            instance (object): L'instance de l'objet qui a déclenché l'événement.
        """
        self.locking = True
        self.actions.check_fingerprint(instance)
        Clock.schedule_interval(self.wait_for_fingerprint, 0.1)

    def wait_for_fingerprint(self, dt):
        """
        Attend que l'authentification par empreinte digitale soit terminée.
        
        Args:
            dt (float): Le temps écoulé depuis la dernière mise à jour de l'horloge.
        
        Returns:
            bool: True si l'attente doit se poursuivre, False sinon.
        """
        if self.fingerprint_done and self.checking_Code:
            self.check_code()
            self.fingerprint_done = False
            return False
        return True

    def identify_fingerprint(self):
        """
        Identifie l'empreinte digitale et effectue les actions nécessaires.
        """
        id = self.model.identify_fingerprint()
        self.current_username = str(id)
        print(self.current_username)
        if id is not None and id >= 0:
            self.actions.handle_fingerprint_match(id)
        else:
            self.actions.handle_fingerprint_mismatch()
        self.model.turn_off_led()
        self.fingerprint_done = True

    def check_code(self):
        """
        Vérifie le code saisi par l'utilisateur.
        """
        self.current_password = ""
        self.view_ops.log_enter_code_message()

    def verify_code(self):
        """
        Vérifie le code saisi.
        """
        self.hashed_password = PasswordOperations.hash_password(self.current_password)
        self.hashed_corect_password = self.password_reader.get_password_for_user(self.current_username)
        if self.hashed_password == self.hashed_corect_password:
            self.view_ops.log_code_correct()
            self.checking_Code = False
            self.Finger_print += self.current_password
            self.handle_crypt()
        else:
            self.view_ops.log_code_incorrect()
            self.check_code()

    def handle_crypt(self):   
        """
        Gère le chiffrement et le déchiffrement des fichiers en fonction de l'état de l'encryption et du verrouillage.
        """
        if self.sharing_state:
            self.view_ops.log_closing_sharing_for_encryption()
            self.stop_samba()
            self.view_ops.log_samba_stop()
        if self.encryption_state and self.unlocking:
            self.view_ops.log_folder_action("Decryptage ")
            self.file_ops.decrypt_folder('/srv/samba/fixedshare')
            self.encryption_state = False
            self.view_ops.log_decrypting_done()
        elif not self.encryption_state and self.locking:
            self.view_ops.log_folder_action("Encryptage ")
            self.file_ops.encrypt_folder('/srv/samba/fixedshare')
            self.encryption_state = True
            self.view_ops.log_encrypting_done()
        elif self.encryption_state and self.locking:
            self.view_ops.log_encryption_already_done()            
        elif not self.encryption_state and self.unlocking:
            self.view_ops.log_decryption_already_done()

    def start_samba(self):
        """
        Démarre le partage Samba.
        """
        if self.sharing_state:
            self.view_ops.log_samba_share_already_open(self.share_name, self.username_share, self.password_share)
            return
        if self.encryption_state:
            self.view_ops.log_you_cant_open()
            return
        elif not self.encryption_state:
            self.sharing_state = True
            self.share_name = random.randint(1, 1000)
            self.username_share, self.password_share = self.samba_manager.create_random_user_and_share(self.share_name)
            self.samba_manager.start_samba()
            self.view_ops.log_samba_start()
            self.view_ops.log_samba_share_created(self.share_name, self.username_share, self.password_share)

    def stop_samba(self):
        """
        Arrête le partage Samba.
        """
        if not self.sharing_state:
            self.view_ops.log_samba_share_already_closed()
            return
        else:
            self.sharing_state = False
            self.samba_manager.stop_samba()
            self.view_ops.log_samba_stop()
            self.samba_manager.remove_random_user_and_share(self.share_name, self.username_share)
            self.share_name = None
            self.username_share = None
            self.password_share = None

    def numpad_button_pressed(self, instance):
        """
        Gère les événements de pression des boutons du pavé numérique.
        
        Args:
            instance (object): L'instance de l'objet qui a déclenché l'événement.
        """
        if self.checking_Code == False:
            return
        else:
            if "C" in instance.text:
                self.current_password = ""
            elif "ok" in instance.text:
                self.verify_code()
            elif instance.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                self.current_password += instance.text

    def get_local_ip(self):
        """
        Récupère l'adresse IP locale de l'appareil.
        
        Returns:
            str: L'adresse IP locale de l'appareil.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = "127.0.0.1"
        finally:
            s.close()
        return local_ip

    def ip_button_pressed(self):
        """
        Gère l'événement de pression du bouton IP.
        """
        ip_address = self.get_local_ip()
        self.view_ops.log_ip_address(ip_address)

    def exit_handler(self):
        """
        Fonction exécutée à la sortie du programme.
        """
        if self.sharing_state:
            self.view_ops.log_samba_stop()            
            self.stop_samba()

        if not self.encryption_state:
            self.view_ops.log_folder_action("Encrypting...")
            self.file_ops.encrypt_folder('/srv/samba/fixedshare')
            self.encryption_state = True
            self.view_ops.log_encrypting_done()

        self.current_username = None
        self.current_password = None
        self.share_name = None
        self.username_share = None
        self.password_share = None
        self.Finger_print = None
        self.checking_Code = False
        self.fingerprint_done = False
        self.encryption_state = False
        self.sharing_state = False

        print("Exiting program...")

    def select_file_encrypt(self):
        """
        Sélectionne un fichier pour le chiffrement.
        """
        self.view_ops.show_file_chooser('encrypt')

    def select_file_decrypt(self):
        """
        Sélectionne un fichier pour le déchiffrement.
        """
        self.view_ops.show_file_chooser('decrypt')
