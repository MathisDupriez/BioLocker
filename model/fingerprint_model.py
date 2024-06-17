# model/fingerprint_model.py
from fingerPrintLib.fplib import fplib

class FingerprintModel:
    def __init__(self, port='/dev/ttyAMA10', baud=9600, timeout=3):
        self.fp_sensor = fplib(port=port, baud=baud, timeout=timeout)
        self.fp_sensor.init()


    def is_finger_pressed(self):
        return self.fp_sensor.is_finger_pressed()
    
    def turn_on_led(self):
        led = self.fp_sensor.set_led(True)

    def turn_off_led(self):
        led = self.fp_sensor.set_led(False)

    
    def identify_fingerprint(self):
        id = self.fp_sensor.identify()
        return id

    def get_template_by_check(self, id_to_retrieve):
        try:
            template, status = self.fp_sensor.get_template(id_to_retrieve)
            if status:
                template_str = template.hex()
                print(template)
                print(template_str)
                return template_str
            else:
                return "erreur lors de la récupération de l'empreinte."
        except ValueError:
            return "Veuillez utilisé le bon doigt"