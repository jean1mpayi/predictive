from datetime import datetime
from typing import Any

from .alerts import build_alert
from .faults import detect_fault
from .confidence import calculate_confidence
from .health import calculate_health
from .history import AnalysisHistory
from .recommendations import build_recommendation
from .rul import calculate_rul


class MaintenanceEngine:
    def __init__(self):
        self.history = AnalysisHistory()
        self.last_sensor_data: dict[str, Any] | None = None
        self.last_analysis: dict[str, Any] | None = None

    def analyze(self, sensor_data):
        self.last_sensor_data = dict(sensor_data)

        health_result = calculate_health(sensor_data)
        fault_result = detect_fault(sensor_data)

        health_value = health_result.value
        fault_name = fault_result["fault"]
        probability = fault_result["probability"]
        confidence = calculate_confidence(health_value, fault_name, probability)

        alert = build_alert(health_value, probability)
        rul = calculate_rul(health_value, fault_name)
        recommendation = build_recommendation(fault_name, health_value, probability)

        result = {
            "health": health_value,
            "health_result": health_result.to_dict(),
            "status": alert["status"],
            "alert": alert,
            "fault": fault_name,
            "probability": probability,
            "confidence": confidence,
            "rul": rul,
            "recommendation": recommendation,
        }

        self.last_analysis = result
        self.history.add(result)
        return result

    def build_payload(
        self,
        *,
        motor=None,
        simulation=None,
        machine=None,
        timestamp=None,
        sensor_data=None,
    ):
        """Build the dashboard-ready payload.

        The method reuses the last analysis by default so the dashboard only
        needs to display the JSON returned by the backend.
        """

        analysis = self.last_analysis
        if analysis is None:
            raise ValueError("No maintenance analysis available. Call analyze() first.")

        payload_sensor_data = sensor_data or self.last_sensor_data or {}
        payload_motor = self._build_motor_block(motor, payload_sensor_data)

        return {
            "timestamp": timestamp or datetime.now().isoformat(),
            "simulation": self._build_simulation_block(simulation, analysis),
            "machine": self._build_machine_block(machine),
            "motor": payload_motor,
            "sensors": self._build_sensor_block(payload_sensor_data),
            "maintenance": self._build_maintenance_block(analysis),
        }

    @staticmethod
    def _build_machine_block(machine):
        default_machine = {
            "id": "MOTOR-01",
            "name": "Synchronous Motor",
            "line": "Bouchonnage",
        }
        if machine:
            default_machine.update(machine)
        return default_machine

    @staticmethod
    def _build_simulation_block(simulation, analysis):
        default_simulation = {
            "running": True,
            "mode": "SIMULATION",
            "fault": MaintenanceEngine._format_fault_name(analysis["fault"]),
        }
        if simulation:
            default_simulation.update(simulation)
            if "fault" in simulation:
                default_simulation["fault"] = MaintenanceEngine._format_fault_name(
                    simulation["fault"]
                )
        return default_simulation

    @staticmethod
    def _build_motor_block(motor, sensor_data):
        if motor is not None:
            return {
                "load": round(float(getattr(motor, "load", 0.0)), 2),
                "wear": round(float(getattr(motor, "wear", 0.0)), 2),
                "misalignment": round(float(getattr(motor, "misalignment", 0.0)), 2),
                "cooling_efficiency": round(
                    float(getattr(motor, "cooling_efficiency", 0.0)),
                    2,
                ),
                "runtime": round(float(getattr(motor, "runtime", 0.0)), 2),
            }

        return {
            "load": round(float(sensor_data.get("load", 0.0) or 0.0), 2),
            "wear": round(float(sensor_data.get("wear", 0.0) or 0.0), 2),
            "misalignment": round(float(sensor_data.get("misalignment", 0.0) or 0.0), 2),
            "cooling_efficiency": 100.0,
            "runtime": round(float(sensor_data.get("runtime", 0.0) or 0.0), 2),
        }

    @staticmethod
    def _build_sensor_block(sensor_data):
        return {
            "temperature": round(float(sensor_data.get("temperature", 0.0) or 0.0), 2),
            "current": round(float(sensor_data.get("current", 0.0) or 0.0), 2),
            "speed": round(float(sensor_data.get("speed", 0.0) or 0.0), 2),
            "torque": round(float(sensor_data.get("torque", 0.0) or 0.0), 2),
            "vibration": round(float(sensor_data.get("vibration", 0.0) or 0.0), 3),
        }

    @staticmethod
    def _build_maintenance_block(analysis):
        return {
            "health": analysis["health"],
            "status": analysis["status"],
            "fault": analysis["fault"],
            "probability": analysis["probability"],
            "confidence": analysis["confidence"],
            "recommendation": analysis["recommendation"],
            "rul": {
                "hours": analysis["rul"]["hours"],
                "days": int(round(analysis["rul"]["days"])),
            },
            "alert": analysis["alert"],
        }

    @staticmethod
    def _format_fault_name(value):
        if not value:
            return "Normal"

        if isinstance(value, str) and ("_" in value or value.isupper()):
            return value.replace("_", " ").title()

        return value
