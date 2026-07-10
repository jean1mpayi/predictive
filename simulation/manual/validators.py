"""
simulation/manual/validators.py

Validation des valeurs de paramètres avant leur application au moteur.

Règles :
- Les bornes sont dérivées des paramètres physiques (physics.py) sans le modifier.
- Une ValueError claire est levée si la valeur est hors plage.
- Chaque validateur est une méthode statique indépendante.
- Compatible avec les futures extensions (multi-moteurs, ML).
"""

from __future__ import annotations

from typing import ClassVar


class ValidationError(ValueError):
    """
    Exception levée lorsqu'une valeur de paramètre est hors des limites
    autorisées pour le contrôle manuel.

    Attributes:
        parameter: Nom du paramètre invalide.
        value: Valeur rejetée.
        min_val: Borne inférieure autorisée.
        max_val: Borne supérieure autorisée.
    """

    def __init__(
        self,
        parameter: str,
        value: float,
        min_val: float,
        max_val: float,
    ) -> None:
        self.parameter = parameter
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        super().__init__(
            f"[ManualControl] Paramètre '{parameter}' invalide : "
            f"valeur={value} hors de [{min_val}, {max_val}]."
        )


class ManualValidator:
    """
    Valide les valeurs avant application manuelle sur le moteur.

    Chaque méthode vérifie qu'une valeur est dans la plage opérationnelle
    sûre. Les bornes sont cohérentes avec physics.py.

    Utilisation :
        ManualValidator.validate("vibration", 2.3)  # OK
        ManualValidator.validate("vibration", 9.9)  # lève ValidationError
    """

    # ------------------------------------------------------------------
    # Table des plages valides par paramètre
    # Format : paramètre -> (min, max, unité)
    # ------------------------------------------------------------------

    RANGES: ClassVar[dict[str, tuple[float, float, str]]] = {
        # Paramètres d'état interne du moteur
        "temperature":        (0.0,   130.0,  "°C"),
        "load":               (0.0,   100.0,  "%"),
        "wear":               (0.0,   100.0,  "%"),
        "misalignment":       (0.0,   100.0,  "%"),
        "cooling_efficiency": (0.0,   100.0,  "%"),

        # Grandeurs physiques directement overridables
        "vibration":          (0.0,   5.0,    "g"),
        "current":            (0.0,   30.0,   "A"),
        "speed":              (0.0,   3000.0, "rpm"),
        "torque":             (0.0,   200.0,  "N.m"),
    }

    # Paramètres qui font partie de RANGES
    VALID_PARAMETERS: ClassVar[frozenset[str]] = frozenset(RANGES.keys())

    # ------------------------------------------------------------------
    # Interface publique
    # ------------------------------------------------------------------

    @classmethod
    def validate(cls, parameter: str, value: float) -> None:
        """
        Valide qu'un paramètre et sa valeur sont acceptables.

        Args:
            parameter: Nom du paramètre (ex: "vibration").
            value: Valeur numérique proposée.

        Raises:
            ValueError: Si le paramètre est inconnu.
            ValidationError: Si la valeur est hors plage.
        """
        cls._check_parameter_known(parameter)
        cls._check_range(parameter, value)

    @classmethod
    def is_valid_parameter(cls, parameter: str) -> bool:
        """Retourne True si le paramètre est reconnu par le système."""
        return parameter in cls.VALID_PARAMETERS

    @classmethod
    def get_range(cls, parameter: str) -> tuple[float, float, str]:
        """
        Retourne (min, max, unité) pour un paramètre donné.

        Raises:
            ValueError: Si le paramètre est inconnu.
        """
        cls._check_parameter_known(parameter)
        return cls.RANGES[parameter]

    # ------------------------------------------------------------------
    # Validateurs individuels (peuvent être appelés directement)
    # ------------------------------------------------------------------

    @staticmethod
    def validate_temperature(value: float) -> None:
        """Vérifie que la température est entre 0 et 130 °C."""
        ManualValidator._check_range("temperature", value)

    @staticmethod
    def validate_load(value: float) -> None:
        """Vérifie que la charge est entre 0 et 100 %."""
        ManualValidator._check_range("load", value)

    @staticmethod
    def validate_vibration(value: float) -> None:
        """Vérifie que la vibration est entre 0 et 5 g."""
        ManualValidator._check_range("vibration", value)

    @staticmethod
    def validate_current(value: float) -> None:
        """Vérifie que le courant est entre 0 et 30 A."""
        ManualValidator._check_range("current", value)

    @staticmethod
    def validate_speed(value: float) -> None:
        """Vérifie que la vitesse est entre 0 et 3000 rpm."""
        ManualValidator._check_range("speed", value)

    @staticmethod
    def validate_torque(value: float) -> None:
        """Vérifie que le couple est entre 0 et 200 N.m."""
        ManualValidator._check_range("torque", value)

    @staticmethod
    def validate_wear(value: float) -> None:
        """Vérifie que l'usure est entre 0 et 100 %."""
        ManualValidator._check_range("wear", value)

    @staticmethod
    def validate_misalignment(value: float) -> None:
        """Vérifie que le désalignement est entre 0 et 100 %."""
        ManualValidator._check_range("misalignment", value)

    @staticmethod
    def validate_cooling_efficiency(value: float) -> None:
        """Vérifie que le rendement de refroidissement est entre 0 et 100 %."""
        ManualValidator._check_range("cooling_efficiency", value)

    # ------------------------------------------------------------------
    # Méthodes internes
    # ------------------------------------------------------------------

    @classmethod
    def _check_parameter_known(cls, parameter: str) -> None:
        """Lève ValueError si le paramètre n'est pas dans RANGES."""
        if parameter not in cls.VALID_PARAMETERS:
            known = ", ".join(sorted(cls.VALID_PARAMETERS))
            raise ValueError(
                f"[ManualControl] Paramètre inconnu : '{parameter}'. "
                f"Paramètres valides : {known}."
            )

    @classmethod
    def _check_range(cls, parameter: str, value: float) -> None:
        """Lève ValidationError si value est hors [min, max]."""
        min_val, max_val, _ = cls.RANGES[parameter]
        if not (min_val <= value <= max_val):
            raise ValidationError(parameter, value, min_val, max_val)
