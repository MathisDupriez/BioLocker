
from kivy.app import App
from controller.main_controller import FingerprintController
from view.main_view import MainView
from model.fingerprint_model import FingerprintModel
from controller.samba_controller import SambaController

class MyApp(App):
    def build(self):
        model = FingerprintModel()
        view = MainView()  # Initially no controller is set
        controller = FingerprintController(model, view)
        view.setup(controller)
        
        return view

if __name__ == '__main__':
    MyApp().run()
