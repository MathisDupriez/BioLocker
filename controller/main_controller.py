from kivy.clock import Clock
from controller.samba_controller import SambaManager
from controller.utils.fingerprint_action import FingerprintActions
from controller.utils.file_opérations import FileOperations
from controller.utils.view_opérations import ViewOperations
from controller.utils.password_opérations import PasswordOperations
from model.password_model import PasswordReader
import socket


class FingerprintController:
    """
    Controller class for fingerprint authentication.
    """

    def __init__(self, model, view, samba_manager):
        self.model = model
        self.view = view
        self.fingerprint_done = False
        self.code_entered = ""
        self.Finger_print = None
        self.checking_Code = False
        self.current_username = None
        self.current_password = None

        self.samba_manager = samba_manager
        self.view_ops = ViewOperations(view)
        self.actions = FingerprintActions(model, self.view_ops, self)
        self.file_ops = FileOperations(self.view_ops, self)
        self.password_reader = PasswordReader('/home/mathis/project/micro-system2024b2q2-main/model/userDb.json')

    
    # Méthode pour déverrouiller le système
    def unlock(self, instance):
        """
        Unlock the system using fingerprint authentication.
        """
        self.actions.check_fingerprint(instance)
        Clock.schedule_interval(self.wait_for_fingerprint, 0.1)

    def wait_for_fingerprint(self, dt):
        """
        Wait for fingerprint authentication to complete.
        """
        if self.fingerprint_done and self.checking_Code:
            self.check_code()
            self.fingerprint_done = False
            return False
        return True

    def identify_fingerprint(self):
        """
        Identify the fingerprint and perform necessary actions.
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


    # Méthode pour crypter et décrypter un dossier
    def encrypt_folder(self):
        self.file_ops.encrypt_folder()

    def decrypt_folder(self):
        self.file_ops.decrypt_folder()


    # Méthode pour vérifier le code
    def check_code(self):
        """
        Check the code entered by the user.
        """
        self.current_password = ""
        self.view_ops.log_enter_code_message()

    def verify_code(self):
        """
        Verify the entered code.
        """
        self.hashed_password = PasswordOperations.hash_password(self.current_password)
        self.hashed_corect_password = self.password_reader.get_password_for_user(self.current_username)
        if self.hashed_password == self.hashed_corect_password:
            self.view_ops.log_code_correct()
            self.checking_Code = False
            self.Finger_print += self.current_password
            #decrypter le dossier ici avant d'ouvrir
            # Utilisation correcte de create_random_user_and_share pour obtenir un nom d'utilisateur et un mot de passe
            share_name = 12
            username, password = self.samba_manager.create_random_user_and_share(share_name)
            self.samba_manager.start_samba()
            self.view_ops.log_samba_start()
            self.view_ops.log_samba_share_created(share_name, username, password)

        else:
            self.view_ops.log_code_incorrect()
            self.check_code()



    # Méthodes pour gérer les événements des boutons
    def numpad_button_pressed(self, instance):
        """
        Handle button press events from the numpad.
        """
        if(self.checking_Code == False):
            return
        else:
            if "C" in instance.text:
                self.current_password = ""
            elif "ok" in instance.text:
                self.verify_code()
            elif instance.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                self.current_password += instance.text


    def menu_button_pressed(self):
        """
        Handle the press event of the menu button.
        """
        self.view_ops.log_menu_button_pressed()

    def settings_button_pressed(self):
        """
        Handle the press event of the settings button.
        """
        self.view_ops.log_settings_button_pressed()

    def get_local_ip(self):
        """
        Retrieve the local IP address of the device.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connexion fictive
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = "127.0.0.1"
        finally:
            s.close()
        return local_ip

    def ip_button_pressed(self):
        """
        Handle the press event of the IP button.
        """
        ip_address = self.get_local_ip()
        self.view_ops.log_ip_address(ip_address)





    # Méthodes pour crypter et décrypter un fichier
    # Non utilisées dans l'application actuelle

    def select_file_encrypt(self):
        """
        Select a file for encryption.
        """
        self.view_ops.show_file_chooser('encrypt')

    def select_file_decrypt(self):
        """
        Select a file for decryption.
        """
        self.view_ops.show_file_chooser('decrypt')
