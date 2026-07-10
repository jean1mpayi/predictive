function bootDashboard() {
    DashboardAPI.start();
    Simulation.init();
    ManualControl.init();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootDashboard);
} else {
    bootDashboard();
}

window.DashboardAPI  = DashboardAPI;
window.Simulation    = Simulation;
window.ManualControl = ManualControl;
