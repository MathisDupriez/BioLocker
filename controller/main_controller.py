import threading
import time
from kivy.clock import Clock
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from controller.crypt_controller import FolderEncryptor
import hashlib
import base64

class FingerprintController:
    """
    Controller class for fingerprint authentication.

    Args:
        model: The model object.
        view: The view object.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.fingerprint_done = False
        self.code_entered = ""
        self.Finger_print = None
        self.checking_Code = False

    def unlock(self, instance):
        """
        Unlock the system using fingerprint authentication.

        Args:
            instance: The instance triggering the unlock action.
        """
        self.check_fingerprint(instance)
        Clock.schedule_interval(self.wait_for_fingerprint, 0.1)

    def wait_for_fingerprint(self, dt):
        """
        Wait for fingerprint authentication to complete.

        Args:
            dt: The time interval between checks.

        Returns:
            bool: True if fingerprint authentication is still in progress, False otherwise.
        """
        if self.fingerprint_done:
            self.check_code()
            self.fingerprint_done = False
            return False
        return True

    def check_fingerprint(self, instance):
        """
        Check the fingerprint for authentication.

        Args:
            instance: The instance triggering the fingerprint check.
        """
        thread = threading.Thread(target=self.run_fingerprint_check, args=(instance,))
        thread.daemon = True
        thread.start()

    def run_fingerprint_check(self, instance):
        """
        Run the fingerprint authentication process.

        Args:
            instance: The instance triggering the fingerprint check.
        """
        self.view.add_log("Procédure de dévérouillage lancée.")
        self.view.add_log("Veuillez poser votre doigt et le laisser jusqu'à l'extinction de la lumière du capteur.")
        self.model.turn_on_led()

        start_time = time.time()
        finger_detected = False

        def check_finger(*args):
            nonlocal finger_detected
            elapsed_time = time.time() - start_time
            time_remaining = 15 - int(elapsed_time)
            if elapsed_time >= 15:
                Clock.unschedule(check_finger)
                if not finger_detected:
                    self.view.add_log("Aucun doigt détecté sur le capteur.")
                    self.view.add_log("Procédure de dévérouillage avortée.")
                    self.model.turn_off_led()
                    self.fingerprint_done = True
                return False

            if self.model.is_finger_pressed():
                finger_detected = True
                Clock.unschedule(check_finger)

            if finger_detected:
                self.identify_fingerprint()
                return False

            self.view.add_log(f"Posez votre doigt, temps restant : {time_remaining} secondes...")
            return True

        Clock.schedule_interval(check_finger, 0.5)

    def identify_fingerprint(self):
        """
        Identify the fingerprint and perform necessary actions.

        This method decrypts a folder if the fingerprint matches.

        """
        id = self.model.identify_fingerprint()
        if id is not None and id >= 0:
            template = self.model.get_template_by_check(id)
            print(template)
            self.Finger_print = template
            self.checking_Code = True

            empreinte_hex = self.Finger_print
            empreinte_bytes = bytes.fromhex(empreinte_hex)
            hachage = hashlib.sha256(empreinte_bytes).digest()
            cle_fernet = base64.urlsafe_b64encode(hachage)
            encryptor = FolderEncryptor(cle_fernet)
            print("Encrypting file...")
            encryptor.decrypt_folder('/home/mathis/project/testencrypt')
            print("File encrypted")

            self.view.add_log("Correspondance d'empreinte trouvée.", "success")
            self.view.change_main_button_text("Déverrouillé.")
        else:
            self.view.add_log("Aucune empreinte correspondante trouvée.", "error")
            self.view.add_log("Procédure de déverrouillage avortée.", "error")
        self.model.turn_off_led()
        self.fingerprint_done = True

    def check_code(self):
        """
        Check the code entered by the user.

        This method prompts the user to enter a 6-digit code.
        """
        self.code_entered = ""
        self.view.add_log("Entrez désormais votre code à 6 chiffres.")

    def numpad_button_pressed(self, instance):
        """
        Handle button press events from the numpad.

        Args:
            instance: The instance of the button pressed.
        """
        if len(self.code_entered) < 6:
            self.code_entered += instance.text
            self.view.add_log(instance.text)
            if self.checking_Code:
                if len(self.code_entered) == 6:
                    self.verify_code()

    def verify_code(self):
        """
        Verify the entered code.

        This method compares the entered code with the correct code and logs the result.
        """
        self.view.add_log(f"Code saisi : {self.code_entered}")
        if self.code_entered == "123456":
            self.view.add_log("Code correct, déverrouillage réussi.", "success")
        else:
            self.view.add_log("Code incorrect, veuillez réessayer.", "error")
        self.code_entered = ""

    def menu_button_pressed(self):
        """
        Handle the press event of the menu button.
        """
        self.view.add_log("Menu button pressed")

    def settings_button_pressed(self):
        """
        Handle the press event of the settings button.
        """
        self.view.add_log("Settings button pressed")

    def help_button_pressed(self):
        """
        Handle the press event of the help button.
        """
        self.view.add_log("Help button pressed")

    def select_file_encrypt(self):
        """
        Select a file for encryption.
        """
        self.show_file_chooser('encrypt')

    def select_file_decrypt(self):
        """
        Select a file for decryption.
        """
        self.show_file_chooser('decrypt')
