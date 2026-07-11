"""
api/views_manual.py

Endpoints REST pour le système de contrôle manuel du moteur.

Architecture :
    Dashboard (POST JSON)
        ↓
    views_manual (parse + délègue)
        ↓
    get_engine().manual  (ManualController)
        ↓
    SynchronousMotor (état interne modifié)
        ↓
    Cycle simulation suivant → Sensors → MaintenanceEngine

Ces views ne contiennent AUCUNE logique métier.
Toute validation est faite dans ManualController/ManualValidator.
"""

from __future__ import annotations

import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from simulation.services.runtime import get_engine
from simulation.manual.validators import ValidationError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# /api/manual/update/
# ---------------------------------------------------------------------------

@csrf_exempt
@require_POST
def manual_update(request) -> JsonResponse:
    """
    Applique une nouvelle valeur manuelle à un paramètre du moteur.

    Body JSON:
        {
            "parameter": "vibration",
            "value": 2.3
        }

    Réponse (succès):
        {
            "success": true,
            "parameter": "vibration",
            "value": 2.3
        }

    Réponse (erreur):
        {
            "success": false,
            "error": "..."
        }
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError) as exc:
        return JsonResponse(
            {"success": False, "error": f"JSON invalide : {exc}"},
            status=400,
        )

    parameter = body.get("parameter", "").strip().lower()
    value = body.get("value")

    # Validation basique des champs présents
    if not parameter:
        return JsonResponse(
            {"success": False, "error": "Champ 'parameter' manquant."},
            status=400,
        )
    if value is None:
        return JsonResponse(
            {"success": False, "error": "Champ 'value' manquant."},
            status=400,
        )

    try:
        value = float(value)
    except (TypeError, ValueError):
        return JsonResponse(
            {"success": False, "error": f"'value' doit être numérique, reçu : {value!r}"},
            status=400,
        )

    # Application via ManualController
    try:
        engine = get_engine()
        engine.manual.set_parameter(parameter, value)

        logger.info("[API/manual] update '%s' → %.4f", parameter, value)

        return JsonResponse({
            "success":   True,
            "parameter": parameter,
            "value":     value,
        })

    except ValidationError as exc:
        return JsonResponse(
            {"success": False, "error": str(exc)},
            status=422,
        )
    except ValueError as exc:
        return JsonResponse(
            {"success": False, "error": str(exc)},
            status=400,
        )
    except Exception as exc:
        logger.exception("[API/manual] Erreur inattendue sur update")
        return JsonResponse(
            {"success": False, "error": "Erreur interne du serveur."},
            status=500,
        )


# ---------------------------------------------------------------------------
# /api/manual/mode/
# ---------------------------------------------------------------------------

@csrf_exempt
@require_POST
def manual_mode(request) -> JsonResponse:
    """Change le mode de contrôle entre AUTO et MANUAL."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError) as exc:
        return JsonResponse(
            {"success": False, "error": f"JSON invalide : {exc}"},
            status=400,
        )

    mode = body.get("mode", "").strip().upper()
    if not mode:
        return JsonResponse(
            {"success": False, "error": "Champ 'mode' manquant."},
            status=400,
        )

    try:
        engine = get_engine()
        engine.manual.set_mode(mode)
        return JsonResponse({
            "success": True,
            "mode": engine.manual.mode.value,
        })
    except ValueError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)
    except Exception as exc:
        logger.exception("[API/manual] Erreur inattendue sur mode")
        return JsonResponse({"success": False, "error": "Erreur interne du serveur."}, status=500)


# ---------------------------------------------------------------------------
# /api/manual/reset/
# ---------------------------------------------------------------------------

@csrf_exempt
@require_POST
def manual_reset(request) -> JsonResponse:
    """
    Réinitialise un paramètre du moteur à sa valeur nominale.

    Body JSON:
        {
            "parameter": "vibration"
        }

    Réponse:
        {
            "success": true,
            "parameter": "vibration",
            "message": "Paramètre 'vibration' réinitialisé."
        }
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError) as exc:
        return JsonResponse(
            {"success": False, "error": f"JSON invalide : {exc}"},
            status=400,
        )

    parameter = body.get("parameter", "").strip().lower()

    if not parameter:
        return JsonResponse(
            {"success": False, "error": "Champ 'parameter' manquant."},
            status=400,
        )

    try:
        engine = get_engine()
        engine.manual.reset_parameter(parameter)

        logger.info("[API/manual] reset '%s'", parameter)

        return JsonResponse({
            "success":   True,
            "parameter": parameter,
            "message":   f"Paramètre '{parameter}' réinitialisé.",
        })

    except ValueError as exc:
        return JsonResponse(
            {"success": False, "error": str(exc)},
            status=400,
        )
    except Exception as exc:
        logger.exception("[API/manual] Erreur inattendue sur reset")
        return JsonResponse(
            {"success": False, "error": "Erreur interne du serveur."},
            status=500,
        )


# ---------------------------------------------------------------------------
# /api/manual/reset_all/
# ---------------------------------------------------------------------------

@csrf_exempt
@require_POST
def manual_reset_all(request) -> JsonResponse:
    """
    Réinitialise TOUS les paramètres du moteur aux valeurs nominales.

    Aucun body nécessaire.

    Réponse:
        {
            "success": true,
            "message": "Tous les paramètres ont été réinitialisés."
        }
    """
    try:
        engine = get_engine()
        engine.manual.reset_all()

        logger.info("[API/manual] reset_all effectué")

        return JsonResponse({
            "success": True,
            "message": "Tous les paramètres ont été réinitialisés.",
        })

    except Exception as exc:
        logger.exception("[API/manual] Erreur inattendue sur reset_all")
        return JsonResponse(
            {"success": False, "error": "Erreur interne du serveur."},
            status=500,
        )


# ---------------------------------------------------------------------------
# /api/manual/snapshot/  (optionnel — debug / ML futur)
# ---------------------------------------------------------------------------

def manual_snapshot(request) -> JsonResponse:
    """
    Retourne l'état actuel des paramètres manuels du moteur.

    Méthode : GET

    Réponse:
        {
            "temperature": 42.5,
            "load": 60.0,
            ...
        }
    """
    try:
        engine = get_engine()
        snapshot = engine.manual.snapshot()
        return JsonResponse({"success": True, "snapshot": snapshot})
    except Exception as exc:
        logger.exception("[API/manual] Erreur sur snapshot")
        return JsonResponse(
            {"success": False, "error": "Erreur interne du serveur."},
            status=500,
        )
