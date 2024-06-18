from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

class ViewOperations:
    def __init__(self, view):
        self.view = view

    def log(self, message, log_type="info"):
        self.view.add_log(message, log_type)

    def log_fingerprint_start(self):
        self.log("Procédure de déverrouillage lancée.")
        self.log("Début de la vérification de l'empreinte digitale.")
        self.log("Veuillez placer votre doigt sur le capteur et le maintenir jusqu'à l'extinction de la lumière.")

    def log_finger_time_remaining(self, time_remaining):
        self.log(f"Temps restant pour placer votre doigt : {time_remaining} secondes.")

    def log_fingerprint_not_detected(self):
        self.log("Aucun doigt détecté sur le capteur. Déverrouillage annulé.", "error")

    def log_enter_code_message(self):
        self.log("Veuillez entrer votre code. Appuyez sur 'ok' pour valider. Appuyez sur 'C' pour effacer.")

    def log_code_entered(self, code):
        self.log(f"Code saisi : {code}")

    def log_code_correct(self):
        self.log("Code correct.", "success")
        self.log("Début de dévérouillage.", "success")

    def log_code_incorrect(self):
        self.log("Code incorrect. Veuillez réessayer.", "error")

    def log_menu_button_pressed(self):
        self.log("Bouton de menu appuyé.")

    def log_settings_button_pressed(self):
        self.log("Bouton des paramètres appuyé.")

    def log_ip_address(self, ip_address):
        self.log(f"Adresse IP de l'appareil : {ip_address}")

    def log_folder_action(self, action, success_message):
        self.log(f"{action.capitalize()} du dossier en cours...")
        self.log(success_message, "success")
    def log_handle_fingerprint_match(self):
        self.log("Correspondance d'empreinte trouvée.", "success")
    
    def log_handle_fingerprint_mismatch(self):
        self.log("Aucune correspondance d'empreinte trouvée.", "error")
        self.log("Procédure avorter.", "error")


    def show_file_chooser(self, action):
        """
        Show the file chooser for the given action.
        """
        chooser = FileChooserListView()
        popup = Popup(title=f"Choisir un fichier à {action}", content=chooser)
        popup.open()
