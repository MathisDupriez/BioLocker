import time
import threading
from kivy.clock import Clock

FINGERPRINT_TIMEOUT = 15

class FingerprintActions:
    """
    Cette classe gère les actions liées à l'empreinte digitale.

    Attributes:
        model (object): L'objet modèle utilisé pour les opérations liées à l'empreinte digitale.
        view_ops (object): L'objet vue utilisé pour les opérations liées à l'interface utilisateur.
        controller (object): L'objet contrôleur utilisé pour les opérations liées à la logique métier.
        start_time (float): Le temps de démarrage de la vérification de l'empreinte digitale.
        finger_detected (bool): Indique si une empreinte digitale a été détectée.

    Methods:
        check_fingerprint(instance): Vérifie l'empreinte digitale pour l'authentification.
        run_fingerprint_check(instance): Exécute le processus d'authentification par empreinte digitale.
        check_finger(dt): Vérifie la présence d'un doigt sur le capteur.
        _handle_fingerprint_timeout(finger_detected): Gère l'expiration du délai d'attente de l'empreinte digitale.
        handle_fingerprint_match(id): Gère la correspondance de l'empreinte digitale avec un identifiant.
        handle_fingerprint_mismatch(): Gère l'absence de correspondance de l'empreinte digitale.
    """
    def __init__(self, model, view_ops, controller):
        self.model = model
        self.view_ops = view_ops
        self.controller = controller
        self.start_time = None
        self.finger_detected = False

    def check_fingerprint(self, instance):
        """
        Vérifie l'empreinte digitale pour l'authentification.
        
        Args:
            instance (object): L'instance de l'objet.

        Returns:
            None
        """
        thread = threading.Thread(target=self.run_fingerprint_check, args=(instance,))
        thread.daemon = True
        thread.start()

    def run_fingerprint_check(self, instance):
        """
        Exécute le processus d'authentification par empreinte digitale.
        
        Args:
            instance (object): L'instance de l'objet.

        Returns:
            None
        """
        self.view_ops.log_fingerprint_start()
        self.model.turn_on_led()

        self.start_time = time.time()
        self.finger_detected = False

        Clock.schedule_interval(self.check_finger, 0.5)

    def check_finger(self, dt):
        """
        Vérifie la présence d'un doigt sur le capteur.
        
        Args:
            dt (float): Le temps écoulé depuis la dernière vérification.

        Returns:
            bool: True si la vérification doit continuer, False sinon.
        """
        elapsed_time = time.time() - self.start_time
        time_remaining = FINGERPRINT_TIMEOUT - int(elapsed_time)

        if elapsed_time >= FINGERPRINT_TIMEOUT:
            Clock.unschedule(self.check_finger)
            self._handle_fingerprint_timeout(self.finger_detected)
            return False

        if self.model.is_finger_pressed():
            self.finger_detected = True
            Clock.unschedule(self.check_finger)
            self.controller.identify_fingerprint()
            return False
        if time_remaining % 5 == 0:
            self.view_ops.log_finger_time_remaining(time_remaining)
        return True

    def _handle_fingerprint_timeout(self, finger_detected):
        """
        Gère l'expiration du délai d'attente de l'empreinte digitale.
        
        Args:
            finger_detected (bool): Indique si une empreinte digitale a été détectée.

        Returns:
            None
        """
        if not finger_detected:
            self.view_ops.log_fingerprint_not_detected()
            self.model.turn_off_led()
            self.controller.fingerprint_done = True

    def handle_fingerprint_match(self, id):
        """
        Gère la correspondance de l'empreinte digitale avec un identifiant.
        
        Args:
            id (int): L'identifiant de l'empreinte digitale correspondante.

        Returns:
            None
        """
        template = self.model.get_template_by_check(id)
        print(template)
        self.controller.Finger_print = template
        self.controller.checking_Code = True
        self.view_ops.log_handle_fingerprint_match()

    def handle_fingerprint_mismatch(self):
        """
        Gère l'absence de correspondance de l'empreinte digitale.
        
        Returns:
            None
        """
        self.view_ops.log_handle_fingerprint_mismatch()
