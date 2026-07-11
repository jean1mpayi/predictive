const Alerts = (() => {
  function update(maintenance) {
    const maintenanceData = maintenance || {};
    const alert = maintenance?.alert || {};
    const recommendation = maintenance?.recommendation || {};
    const rul = maintenance?.rul || {};

    const html = `
            <div class="alert-card alert-${(alert.color || "green").toLowerCase()}">
                <div class="alert-header">
                    <span class="alert-icon">${alert.icon || "✅"}</span>
                    <div>
                        <div class="alert-status">${alert.status || "NORMAL"}</div>
                        <div class="alert-priority">${alert.priority || "LOW"}</div>
                    </div>
                </div>
                <div class="alert-body">
                    <p><strong>Défaut :</strong> ${maintenanceData.fault || "Normal"}</p>
                    <p><strong>Probabilité :</strong> ${maintenanceData.probability ?? 0}%</p>
                    <p><strong>Confiance :</strong> ${maintenanceData.confidence ?? 100}%</p>
                    <p><strong>Durée de vie restante :</strong> ${Number(rul.hours || 0).toFixed(0)} h</p>
                    <p><strong>Action :</strong> ${recommendation.action || "N/A"}</p>
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
