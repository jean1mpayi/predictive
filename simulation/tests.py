from django.test import SimpleTestCase

from simulation.core.motor import SynchronousMotor
from simulation.manual.controller import ManualController


class ManualControlModeTests(SimpleTestCase):
    def test_manual_mode_uses_override_and_auto_restores_physics(self):
        motor = SynchronousMotor()
        controller = ManualController(motor)

        self.assertTrue(controller.is_auto())
        self.assertFalse(controller.is_manual())

        controller.set_mode("MANUAL")
        controller.set_vibration(1.5)

        self.assertTrue(controller.is_manual())
        self.assertEqual(motor.manual_override["vibration"], 1.5)

        motor.running = True
        motor.update(dt=1)
        self.assertEqual(motor.vibration, 1.5)

        controller.set_mode("AUTO")

        self.assertTrue(controller.is_auto())
        self.assertIsNone(motor.manual_override["vibration"])

        motor.update(dt=1)
        self.assertNotEqual(motor.vibration, 1.5)
