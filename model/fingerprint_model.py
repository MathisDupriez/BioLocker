# model/fingerprint_model.py
from fingerPrintLib.fplib import fplib

class FingerprintModel:
    """
    Représente un modèle d'empreinte digitale qui interagit avec un capteur d'empreintes digitales.

    Args:
        port (str, optionnel): Le port auquel le capteur d'empreintes digitales est connecté. Par défaut, '/dev/ttyAMA10'.
        baud (int, optionnel): Le débit en bauds pour la communication avec le capteur d'empreintes digitales. Par défaut, 9600.
        timeout (int, optionnel): La valeur de timeout pour la communication avec le capteur d'empreintes digitales. Par défaut, 3.

    Attributes:
        fp_sensor (fplib): L'objet capteur d'empreintes digitales.
    """

    def __init__(self, port='/dev/ttyAMA10', baud=9600, timeout=3):
        """
        Initialise une nouvelle instance de la classe FingerprintModel.

        Args:
            port (str, optionnel): Le port auquel le capteur d'empreintes digitales est connecté. Par défaut, '/dev/ttyAMA10'.
            baud (int, optionnel): Le débit en bauds pour la communication avec le capteur d'empreintes digitales. Par défaut, 9600.
            timeout (int, optionnel): La valeur de timeout pour la communication avec le capteur d'empreintes digitales. Par défaut, 3.
        """
        self.fp_sensor = fplib(port=port, baud=baud, timeout=timeout)
        self.fp_sensor.init()

    def is_finger_pressed(self):
        """
        Vérifie si un doigt est actuellement pressé sur le capteur d'empreintes digitales.

        Returns:
            bool: True si un doigt est pressé, False sinon.
        """
        return self.fp_sensor.is_finger_pressed()

    def turn_on_led(self):
        """
        Allume la LED du capteur d'empreintes digitales.
        """
        led = self.fp_sensor.set_led(True)

    def turn_off_led(self):
        """
        Turns off the LED of the fingerprint sensor.
        """
        led = self.fp_sensor.set_led(False)

    def identify_fingerprint(self):
        """
        Identifies the fingerprint currently placed on the sensor.

        Returns:
            int: The ID of the identified fingerprint.
        """
        id = self.fp_sensor.identify()
        return id

    def get_template_by_check(self, id_to_retrieve):
        """
        Retrieves the fingerprint template for the given ID.

        Args:
            id_to_retrieve (int): The ID of the fingerprint template to retrieve.

        Returns:
            str: The hexadecimal representation of the fingerprint template.

        Raises:
            ValueError: If the provided ID is invalid.
        """
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