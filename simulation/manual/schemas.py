"""
simulation/manual/schemas.py

Structures de données pour le système de contrôle manuel.
Utilise les dataclasses Python standard (pas de dépendance externe).

Ces schemas servent de contrat entre :
- L'API Django (déserialisation des requêtes JSON)
- Le ManualController (validation et application)
- Futures intégrations ML / multi-moteurs
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# ParameterUpdate
# ---------------------------------------------------------------------------

@dataclass
class ParameterUpdate:
    """
    Représente la mise à jour d'un seul paramètre du moteur.

    Attributes:
        parameter: Nom du paramètre cible (ex: "vibration", "load").
        value: Nouvelle valeur numérique à appliquer.
    """

    parameter: str
    value: float

    def __post_init__(self) -> None:
        """Normalise le nom du paramètre en minuscules."""
        self.parameter = self.parameter.lower().strip()


# ---------------------------------------------------------------------------
# ResetCommand
# ---------------------------------------------------------------------------

@dataclass
class ResetCommand:
    """
    Commande de réinitialisation d'un paramètre ou de tous les paramètres.

    Attributes:
        parameter: Nom du paramètre à réinitialiser.
                   Si None, tous les paramètres sont réinitialisés.
    """

    parameter: Optional[str] = None

    def __post_init__(self) -> None:
        """Normalise le nom si fourni."""
        if self.parameter is not None:
            self.parameter = self.parameter.lower().strip()

    @property
    def is_global_reset(self) -> bool:
        """Retourne True si la commande réinitialise tous les paramètres."""
        return self.parameter is None


# ---------------------------------------------------------------------------
# ManualCommand  (enveloppe générique)
# ---------------------------------------------------------------------------

@dataclass
class ManualCommand:
    """
    Enveloppe générique pour toute commande manuelle.

    Permet de tracer les commandes envoyées (utile pour le ML futur
    et les logs d'audit industriels).

    Attributes:
        action: Type d'action ("update" | "reset" | "reset_all").
        parameter: Paramètre cible (None pour reset_all).
        value: Valeur numérique (None pour les resets).
        source: Origine de la commande (ex: "dashboard", "api", "test").
    """

    action: str
    parameter: Optional[str] = None
    value: Optional[float] = None
    source: str = "dashboard"

    # Paramètres valides reconnus par le système
    VALID_ACTIONS: frozenset = field(
        default_factory=lambda: frozenset({"update", "reset", "reset_all"}),
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.parameter is not None:
            self.parameter = self.parameter.lower().strip()
