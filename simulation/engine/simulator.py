import time
import threading

from simulation.core.motor import SynchronousMotor
from simulation.core.sensors import (
    TemperatureSensor,
    VibrationSensor,
    CurrentSensor,
    TorqueSensor,
    SpeedSensor
)
from simulation.faults import FaultInjector
from simulation.manual.controller import ManualController

from simulation.services.sender import APISender


class SimulationEngine:
    """
    Moteur de simulation industriel temps réel.

    - Tourne dans un thread séparé
    - Met à jour le moteur
    - Lit les capteurs
    - Envoie les données vers l'API
    """

    def __init__(self, interval=1.0, api_enabled=True):

        # -----------------------------
        # Paramètres de simulation
        # -----------------------------
        self.interval = interval
        self.running = False

        # -----------------------------
        # Moteur physique
        # -----------------------------
        self.motor = SynchronousMotor()

        # -----------------------------
        # Capteurs
        # -----------------------------
        self.temp_sensor = TemperatureSensor()
        self.vib_sensor = VibrationSensor()
        self.curr_sensor = CurrentSensor()
        self.torque_sensor = TorqueSensor()
        self.speed_sensor = SpeedSensor()

        # -----------------------------
        # API sender (optionnel)
        # -----------------------------
        self.api_enabled = api_enabled
        self.sender = APISender()

        # -----------------------------
        # Injecteur de panne
        # -----------------------------
        self.fault_injector = FaultInjector()

        # -----------------------------
        # Contrôle manuel (API → moteur)
        # -----------------------------
        self.manual = ManualController(self.motor)

        # -----------------------------
        # Thread
        # -----------------------------
        self.thread = None

    # =====================================================
    # START
    # =====================================================
    def start(self):
        if self.running:
            return

        self.running = True
        self.motor.start()

        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        print("[SIMULATION] démarrée")

    # =====================================================
    # STOP
    # =====================================================
    def stop(self):
        self.running = False
        self.motor.stop()

        print("[SIMULATION] arrêtée")

    # =====================================================
    # PANNE
    # =====================================================
    def set_fault_mode(self, fault_name):
        """Activate a fault scenario for the next simulation cycles."""

        self.fault_injector.activate(fault_name)
        if self.running:
            self.fault_injector.kick(self.motor)

        if fault_name.upper() == "NORMAL" and self.running and self.motor.running is False:
            self.motor.start()

    # =====================================================
    # LOOP PRINCIPALE
    # =====================================================
    def _run(self):
        while self.running:

            # 1. injection de panne interne
            self.fault_injector.update(self.motor)

            # 2. mise à jour moteur physique
            self.motor.update(dt=self.interval)

            # 3. lecture capteurs
            data = self._read_sensors()

            # 4. envoi API (optionnel)
            if self.api_enabled:
                self._send(data)

            # 5. debug console
            self._log(data)

            # 6. attente temps réel
            time.sleep(self.interval)

    # =====================================================
    # CAPTATION
    # =====================================================
    def _read_sensors(self):
        return {
            "temperature": self.temp_sensor.read(self.motor),
            "vibration": self.vib_sensor.read(self.motor),
            "current": self.curr_sensor.read(self.motor),
            "torque": self.torque_sensor.read(self.motor),
            "speed": self.speed_sensor.read(self.motor),

            # données internes utiles pour ML
            "load": self.motor.load,
            "wear": self.motor.wear,
            "misalignment": self.motor.misalignment,

            # indicateur IA
            "health": self.motor.health_index,

            # temps
            "runtime": self.motor.runtime
        }

    # =====================================================
    # ENVOI API
    # =====================================================
    def _send(self, data):
        try:
            self.sender.send(data)
        except Exception as e:
            print("[SIMULATION][ERROR API]", e)

    # =====================================================
    # LOG
    # =====================================================
    def _log(self, data):
        print(
            f"T={data['temperature']}°C | "
            f"Vib={data['vibration']} | "
            f"I={data['current']}A | "
            f"Speed={data['speed']}rpm | "
            f"Health={data['health']}%"
        )
