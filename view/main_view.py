# view/main_view.py
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.clock import Clock

# Configurer la fenêtre pour qu'elle se lance en plein écran
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '320')
Config.set('graphics', 'resizable', False)  # Rendre la fenêtre non redimensionnable
kivy.require('2.1.0')

# Charger le fichier .kv
Builder.load_file('view/main_view.kv')

class MainView(BoxLayout):
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.on_size)  # Bind size changes to the on_size method

    def setup(self, controller):
        self.controller = controller

    def on_size(self, *args):
        for log_label in self.ids.log_box.children:
            log_label.text_size = (self.width * 0.65, None)

    def add_log(self, log_message, log_type="info"):
        Clock.schedule_once(lambda dt: self._add_log(log_message, log_type))

    def _add_log(self, log_message, log_type):
        color = {'info': [1, 1, 1, 1], 'error': [1, 0, 0, 1], 'success': [0, 1, 0, 1]}[log_type]
        log_message = str(log_message)
        # Créez le label et ajoutez-le au conteneur de logs
        log_label = Label(
            text=log_message,
            color=color,
            size_hint_y=None,
            height=20,
            halign='left',
            valign='middle',
            text_size=(self.width * 0.65, None)
        )
        log_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        self.ids.log_box.add_widget(log_label)
        # Scroll to the bottom after adding the new log
        Clock.schedule_once(lambda dt: setattr(self.ids.log_scroll, 'scroll_y', 0))

    def change_main_button_text(self, text):
        self.ids.main_button.text = text
