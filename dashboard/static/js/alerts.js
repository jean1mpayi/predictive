const Alerts = (() => {
  function update(maintenance) {
    const maintenanceData = maintenance || {};
    const alert = maintenance?.alert || {};
    const recommendation = maintenance?.recommendation || {};
    const rul = maintenance?.rul || {};

    const statusLabel = (alert.status || "NORMAL").toUpperCase();
    const priorityLabel = (alert.priority || "FAIBLE").toUpperCase();
    const faultLabel = maintenanceData.fault || "Normal";
    const probabilityValue = maintenanceData.probability ?? 0;
    const confidenceValue = maintenanceData.confidence ?? 100;
    const remainingHours = Number(rul.hours || 0).toFixed(0);
    const actionLabel = recommendation.action || "Aucune action recommandée";

    const html = `
            <div class="alert-card alert-${(alert.color || "green").toLowerCase()}">
                <div class="alert-header">
                    <span class="alert-icon">${alert.icon || "✅"}</span>
                    <div>
                        <div class="alert-status">${statusLabel}</div>
                        <div class="alert-priority">${priorityLabel}</div>
                    </div>
                </div>
                <div class="alert-body">
                    <p><strong>Défaut :</strong> ${faultLabel}</p>
                    <p><strong>Probabilité :</strong> ${probabilityValue}%</p>
                    <p><strong>Confiance :</strong> ${confidenceValue}%</p>
                    <p><strong>Durée de vie restante :</strong> ${remainingHours} h</p>
                    <p><strong>Action :</strong> ${actionLabel}</p>
                </div>
                <div class="alert-footer">${alert.message || ""}</div>
            </div>
        `;

    const container = document.getElementById("alerts");
    if (container) {
      container.innerHTML = html;
    }
  }

  return {
    update,
  };
})();

window.Alerts = Alerts;
