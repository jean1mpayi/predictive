/**
 * manual.js
 *
 * Connecte les sliders du panneau "Réglage manuel" à l'API backend.
 *
 * Comportement :
 * - Chaque slider avec data-param envoie un POST à /api/manual/update/
 *   dès que l'utilisateur relâche le curseur (event "change")
 * - L'affichage de la valeur (span#manualVal-*) est mis à jour en temps réel
 *   pendant le glissement (event "input")
 * - Le bouton Reset All envoie un POST à /api/manual/reset_all/
 * - Aucun calcul dans ce fichier — tout est délégué au backend
 *
 * Architecture respectée :
 *   Dashboard (slider) → POST /api/manual/update/ → ManualController → SynchronousMotor
 */

const ManualControl = (() => {
  // ------------------------------------------------------------------
  // Délai anti-rebond en ms (évite de flooder l'API pendant le glissement)
  // ------------------------------------------------------------------
  const DEBOUNCE_MS = 150;

  // ------------------------------------------------------------------
  // Initialisation
  // ------------------------------------------------------------------

  function init() {
    const sliders = document.querySelectorAll("[data-param]");

    sliders.forEach((slider) => {
      // Mise à jour de l'affichage en temps réel (pendant le glissement)
      slider.addEventListener("input", onSliderInput);

      // Envoi API uniquement quand l'utilisateur relâche (moins de requêtes)
      slider.addEventListener("change", debounce(onSliderChange, DEBOUNCE_MS));
    });

    const resetBtn = document.getElementById("manualResetAllBtn");
    if (resetBtn) {
      resetBtn.addEventListener("click", onResetAll);
    }

    const modeInputs = document.querySelectorAll("input[name='manualMode']");
    modeInputs.forEach((input) => {
      input.addEventListener("change", onModeChange);
    });

    updateManualModeUI("AUTO");

    console.log(
      "[ManualControl] Initialisé —",
      sliders.length,
      "sliders détectés.",
    );
  }

  // ------------------------------------------------------------------
  // Événement : changement de mode AUTO/MANUAL
  // ------------------------------------------------------------------

  async function onModeChange(event) {
    const mode = event.target.value;
    try {
      const response = await fetch("/api/manual/mode/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode }),
      });

      const data = await response.json();
      if (!data.success) {
        console.warn("[ManualControl] Changement de mode échoué :", data.error);
        setBadgeError();
        return;
      }

      updateManualModeUI(data.mode || mode);
      setBadgeOk();

      if (typeof DashboardAPI !== "undefined" && DashboardAPI.refresh) {
        DashboardAPI.refresh();
      }
    } catch (err) {
      console.error("[ManualControl] Erreur réseau mode :", err);
      setBadgeError();
    }
  }

  function updateManualModeUI(mode) {
    const status = document.getElementById("manualModeStatus");
    const autoInput = document.getElementById("manualModeAuto");
    const manualInput = document.getElementById("manualModeManual");

    if (autoInput) autoInput.checked = mode === "AUTO";
    if (manualInput) manualInput.checked = mode === "MANUAL";

    const overrideParameters = [
      "temperature",
      "vibration",
      "current",
      "speed",
      "torque",
    ];
    document.querySelectorAll("[data-param]").forEach((slider) => {
      const param = slider.dataset.param;
      const isOverride = overrideParameters.includes(param);
      slider.disabled = isOverride && mode === "AUTO";
      slider.classList.toggle("opacity-50", isOverride && mode === "AUTO");
      slider.classList.toggle(
        "cursor-not-allowed",
        isOverride && mode === "AUTO",
      );
      slider.classList.toggle(
        "cursor-pointer",
        !(isOverride && mode === "AUTO"),
      );
    });

    if (status) {
      status.textContent =
        mode === "MANUAL"
          ? "Overrides actifs — le moteur suit les valeurs imposées."
          : "Overrides désactivés — calcul physique actif.";
      status.className =
        mode === "MANUAL"
          ? "mt-2 text-[11px] font-medium text-amber-700"
          : "mt-2 text-[11px] font-medium text-cyan-700";
    }
  }

  // ------------------------------------------------------------------
  // Événement : mise à jour affichage (sans appel API)
  // ------------------------------------------------------------------

  function onSliderInput(event) {
    const slider = event.target;
    const param = slider.dataset.param;
    const unit = slider.dataset.unit || "";
    const value = parseFloat(slider.value);

    // Mise à jour du label d'affichage
    const label = document.getElementById(`manualVal-${param}`);
    if (label) {
      label.textContent = `${value.toFixed(param === "vibration" ? 2 : 1)} ${unit}`;
    }
  }

  // ------------------------------------------------------------------
  // Événement : envoi valeur → API backend
  // ------------------------------------------------------------------

  async function onSliderChange(event) {
    const slider = event.target;
    const parameter = slider.dataset.param;
    const value = parseFloat(slider.value);

    try {
      const response = await fetch("/api/manual/update/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ parameter, value }),
      });

      const data = await response.json();

      if (!data.success) {
        console.warn(
          `[ManualControl] Erreur API pour '${parameter}':`,
          data.error,
        );
        setBadgeError();
      } else {
        setBadgeOk();
        // Rafraîchir le dashboard immédiatement après application
        if (typeof DashboardAPI !== "undefined" && DashboardAPI.refresh) {
          DashboardAPI.refresh();
        }
      }
    } catch (err) {
      console.error("[ManualControl] Erreur réseau :", err);
      setBadgeError();
    }
  }

  // ------------------------------------------------------------------
  // Bouton : Reset All
  // ------------------------------------------------------------------

  async function onResetAll() {
    try {
      const response = await fetch("/api/manual/reset_all/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });

      const data = await response.json();

      if (data.success) {
        // Remettre tous les sliders à leur valeur initiale (HTML)
        document.querySelectorAll("[data-param]").forEach((slider) => {
          const defaultValue = slider.defaultValue;
          slider.value = defaultValue;

          // Mettre à jour les labels
          const param = slider.dataset.param;
          const unit = slider.dataset.unit || "";
          const label = document.getElementById(`manualVal-${param}`);
          if (label) {
            label.textContent = `${parseFloat(defaultValue).toFixed(param === "vibration" ? 2 : 1)} ${unit}`;
          }
        });

        setBadgeOk();

        // Rafraîchir le dashboard
        if (typeof DashboardAPI !== "undefined" && DashboardAPI.refresh) {
          DashboardAPI.refresh();
        }

        console.log("[ManualControl] reset_all effectué.");
      } else {
        console.warn("[ManualControl] reset_all échoué :", data.error);
        setBadgeError();
      }
    } catch (err) {
      console.error("[ManualControl] Erreur réseau reset_all :", err);
      setBadgeError();
    }
  }

  // ------------------------------------------------------------------
  // Badge de statut connexion
  // ------------------------------------------------------------------

  function setBadgeOk() {
    const badge = document.getElementById("manualBadge");
    if (!badge) return;
    badge.textContent = "Backend connecté";
    badge.classList.remove(
      "border-rose-400/30",
      "bg-rose-400/10",
      "text-rose-300",
    );
    badge.classList.add(
      "border-cyan-400/20",
      "bg-cyan-400/10",
      "text-cyan-200",
    );
  }

  function setBadgeError() {
    const badge = document.getElementById("manualBadge");
    if (!badge) return;
    badge.textContent = "Erreur connexion";
    badge.classList.remove(
      "border-cyan-400/20",
      "bg-cyan-400/10",
      "text-cyan-200",
    );
    badge.classList.add(
      "border-rose-400/30",
      "bg-rose-400/10",
      "text-rose-300",
    );
  }

  // ------------------------------------------------------------------
  // Utilitaire : anti-rebond (debounce)
  // ------------------------------------------------------------------

  function debounce(fn, delay) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  // ------------------------------------------------------------------
  // API publique
  // ------------------------------------------------------------------

  return {
    init,
  };
})();

window.ManualControl = ManualControl;
