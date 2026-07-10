"""Fault injection package for the industrial simulation layer."""

from .injector import FaultInjector
from .scenarios import FAULT_SCENARIOS

__all__ = ["FaultInjector", "FAULT_SCENARIOS"]

