
from kivy.app import App
from controller.main_controller import FingerprintController
from view.main_view import MainView
from model.fingerprint_model import FingerprintModel
from controller.samba_controller import SambaManager

class BioLocker(App):
    """Classe représentant l'application MyApp.

    Cette classe est utilisée pour créer et configurer l'application MyApp.
    Elle hérite de la classe App du framework Kivy.

    Attributes:
        sambaManager: Objet SambaManager pour gérer le partage de fichiers.
        model: Objet FingerprintModel pour gérer les données de l'empreinte digitale.
        view: Objet MainView pour afficher l'interface utilisateur.
        controller: Objet FingerprintController pour gérer la logique métier.
        
    Methods:
        build: Méthode pour construire et configurer l'application.
    """

    def build(self):
        sambaManager = SambaManager()
        model = FingerprintModel()
        view = MainView()  # Initially no controller is set
        controller = FingerprintController(model, view, sambaManager)
        view.setup(controller)
        sambaManager.stop_samba()
        return view

if __name__ == '__main__':
    BioLocker().run()
