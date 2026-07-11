/**
 * NotificationManager
 * Gère les notifications Toastify pour le système SCADA.
 * Affiche les notifications uniquement sur les changements d'état (front montant/descendant).
 */
const NotificationManager = (() => {
  // Variables d'état pour éviter les doublons (spam)
  let lastStatus = null;
  let lastFault = null;
  let lastHealthThreshold = null; // 100, 80, 50, 0
  let lastRunningState = null;

  // Palette de couleurs
  const COLORS = {
    INFO: "#3B82F6",
    SUCCESS: "#22C55E",
    WARNING: "#F59E0B",
    ERROR: "#EF4444",
    CRITICAL: "#991B1B",
  };

  /**
   * Affiche un toast via Toastify JS
   */
  function showToast(title, message, icon, color) {
    Toastify({
      text: `
                <div style="display: flex; gap: 12px; align-items: start;">
                    <div style="font-size: 1.5rem;">${icon}</div>
                    <div>
                        <strong style="display: block; font-size: 1.05rem; margin-bottom: 4px;">${title}</strong>
                        <span style="font-size: 0.9rem; opacity: 0.9; line-height: 1.4;">${message}</span>
                    </div>
                </div>
            `,
      duration: 5000,
      close: true,
      gravity: "top", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      escapeMarkup: false, // Allow HTML
      style: {
        background: color,
        borderRadius: "12px",
        padding: "16px 20px",
        boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.2)",
        minWidth: "300px",
        maxWidth: "400px",
        color: "#ffffff",
      },
    }).showToast();
  }

  /**
   * Calcule le palier de santé actuel
   */
  function getHealthThreshold(health) {
    if (health <= 0) return 0;
    if (health < 50) return 50;
    if (health < 80) return 80;
    return 100;
  }

  /**
   * Point d'entrée principal appelé par l'API
   */
  function update(payload) {
    if (!payload) return;

    const maintenance = payload.maintenance || {};
    const simulation = payload.simulation || {};

    const currentStatus = maintenance.status || "NORMAL";
    const currentHealth =
      maintenance.health !== undefined ? maintenance.health : 100;
    const currentFault = maintenance.fault || "NORMAL";
    const currentRunningState = simulation.running;

    // ----------------------------------------------------
    // 1 & 2. Changement d'état de la simulation (Start/Stop)
    // ----------------------------------------------------
    if (lastRunningState !== null && lastRunningState !== currentRunningState) {
      if (currentRunningState === true) {
        showToast(
          "Simulation démarrée",
          "La simulation industrielle a démarré avec succès.",
          "▶️",
          COLORS.INFO,
        );
      } else {
        showToast(
          "Simulation arrêtée",
          "La simulation a été arrêtée.",
          "⏹",
          "#6B7280", // Gris
        );
      }
    }
    lastRunningState = currentRunningState;

    // ----------------------------------------------------
    // 3, 4, 5. Changement de statut global (NORMAL / WARNING / CRITICAL)
    // ----------------------------------------------------
    if (lastStatus !== null && lastStatus !== currentStatus) {
      if (currentStatus === "NORMAL") {
        showToast(
          "Système normal",
          "La machine fonctionne normalement.",
          "✅",
          COLORS.SUCCESS,
        );
      } else if (currentStatus === "WARNING") {
        const prob =
          maintenance.probability !== undefined
            ? `${maintenance.probability.toFixed(1)} %`
            : "N/A";
        showToast(
          `Alerte de panne : ${currentStatus}`,
          `<strong>Défaut :</strong> ${currentFault}<br/><strong>Santé :</strong> ${currentHealth.toFixed(1)} %<br/><strong>Probabilité :</strong> ${prob}`,
          "⚠️",
          COLORS.WARNING,
        );
      } else if (currentStatus === "CRITICAL") {
        const action =
          maintenance.recommendation && maintenance.recommendation.action
            ? maintenance.recommendation.action
            : "Une inspection immédiate est requise.";
        showToast(
          `Avertissement : ${currentStatus}`,
          `<strong>Défaut :</strong> ${currentFault}<br/><strong>Santé :</strong> ${currentHealth.toFixed(1)} %<br/><strong>Action :</strong> ${action}`,
          "🚨",
          COLORS.CRITICAL,
        );
      }
    }
    lastStatus = currentStatus;

    // ----------------------------------------------------
    // 9. Nouvelle panne détectée
    // ----------------------------------------------------
    if (
      lastFault !== null &&
      lastFault !== currentFault &&
      currentFault !== "NORMAL"
    ) {
      // Si la panne change et n'est pas juste un retour à la normale
      showToast("Détection de panne", currentFault, "🚨", COLORS.ERROR);
    }
    lastFault = currentFault;

    // ----------------------------------------------------
    // 6, 7, 8. Paliers de dégradation de la santé (Health)
    // ----------------------------------------------------
    const currentThreshold = getHealthThreshold(currentHealth);

    if (
      lastHealthThreshold !== null &&
      currentThreshold < lastHealthThreshold
    ) {
      // La santé vient de franchir un palier vers le bas
      if (currentThreshold === 80) {
        showToast(
          "Santé en baisse",
          "La santé est passée sous 80 %.",
          "⚠️",
          COLORS.WARNING,
        );
      } else if (currentThreshold === 50) {
        showToast(
          "Dégradation de la machine",
          "La santé est sous le seuil critique.",
          "🚨",
          COLORS.ERROR,
        );
      } else if (currentThreshold === 0) {
        showToast(
          "Panne de la machine",
          "La machine a atteint l'état de panne.",
          "💥",
          COLORS.CRITICAL,
        );
      }
    }
    lastHealthThreshold = currentThreshold;
  }

  return {
    update,
  };
})();

window.NotificationManager = NotificationManager;
