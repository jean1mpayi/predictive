from django.test import TestCase

from predictive.alerts import build_alert


class AlertTranslationTests(TestCase):
    def test_build_alert_returns_french_messages(self):
        warning_alert = build_alert(70, 60)
        critical_alert = build_alert(20, 90)

        self.assertEqual(warning_alert["status"], "ATTENTION")
        self.assertEqual(warning_alert["message"], "Dégradation détectée, surveiller l’équipement")
        self.assertEqual(critical_alert["status"], "CRITIQUE")
        self.assertEqual(critical_alert["message"], "Maintenance immédiate requise")
