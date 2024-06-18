import time
import threading
from kivy.clock import Clock

FINGERPRINT_TIMEOUT = 15

class FingerprintActions:
    def __init__(self, model, view_ops, controller):
        self.model = model
        self.view_ops = view_ops
        self.controller = controller
        self.start_time = None
        self.finger_detected = False

    def check_fingerprint(self, instance):
        """
        Check the fingerprint for authentication.
        """
        thread = threading.Thread(target=self.run_fingerprint_check, args=(instance,))
        thread.daemon = True
        thread.start()

    def run_fingerprint_check(self, instance):
        """
        Run the fingerprint authentication process.
        """
        self.view_ops.log_fingerprint_start()
        self.model.turn_on_led()

        self.start_time = time.time()
        self.finger_detected = False

        Clock.schedule_interval(self.check_finger, 0.5)

    def check_finger(self, dt):
        """
        Check for the presence of a finger on the sensor.
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
        if not finger_detected:
            self.view_ops.log_fingerprint_not_detected()
            self.model.turn_off_led()
            self.controller.fingerprint_done = True

    def handle_fingerprint_match(self, id):
        template = self.model.get_template_by_check(id)
        print(template)
        self.controller.Finger_print = template
        self.controller.checking_Code = True
        self.view_ops.log_handle_fingerprint_match()

    def handle_fingerprint_mismatch(self):
        self.view_ops.log_handle_fingerprint_mismatch()
