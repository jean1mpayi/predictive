"""Runtime management for the simulation engine.

This module keeps a single background engine instance alive so the Django
buttons can start and stop the digital-twin loop without changing the
simulation architecture.
"""

from __future__ import annotations

from threading import Lock

from simulation.engine.simulator import SimulationEngine
from simulation.models import SimulationConfig


_engine: SimulationEngine | None = None
_lock = Lock()


def get_engine() -> SimulationEngine:
    """Return the singleton simulation engine."""

    global _engine

    with _lock:
        if _engine is None:
            _engine = SimulationEngine(interval=1.0, api_enabled=True)

        return _engine


def start_engine() -> None:
    """Start the singleton engine if it is not already running."""

    engine = get_engine()

    config = SimulationConfig.objects.first()
    if config is not None:
        engine.set_fault_mode(config.fault_mode)

    engine.start()


def stop_engine() -> None:
    """Stop the singleton engine if it is running."""

    global _engine

    with _lock:
        if _engine is not None:
            _engine.stop()


def set_fault_mode(fault_name: str) -> str:
    """Update the running engine and persist the selected fault mode."""

    normalized_name = fault_name.upper()
    config = SimulationConfig.objects.first()
    if config is None:
        config = SimulationConfig.objects.create()

    config.fault_mode = normalized_name
    config.save(update_fields=["fault_mode"])

    engine = get_engine()
    engine.set_fault_mode(normalized_name)
    return normalized_name
