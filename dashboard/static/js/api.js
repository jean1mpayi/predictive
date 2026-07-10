const DashboardAPI = (() => {

    const liveHistory = [];
    const MAX_HISTORY = 12;

    async function updateDashboard(){

        try{

            const response = await fetch("/api/latest/");

            const payload = await response.json();
            const sensors = payload.sensors || payload.sensor || payload;
            const maintenance = payload.maintenance || {};
            const sensorSnapshot = {
                ...sensors,
                health: maintenance.health ?? sensors.health ?? 0
            };

            if (typeof Gauges !== "undefined") {
                Gauges.update(sensorSnapshot);
            }

            if (typeof Charts !== "undefined") {
                Charts.push({
                    temperature: Number(sensors.temperature || 0),
                    vibration: Number(sensors.vibration || 0),
                    current: Number(sensors.current || 0),
                    speed: Number(sensors.speed || 0),
                    torque: Number(sensors.torque || 0),
                    health: Number(maintenance.health ?? sensors.health ?? 0)
                });
            }

            if (typeof Alerts !== "undefined") {
                Alerts.update(maintenance);
            }

            if (typeof History !== "undefined") {
                appendLiveMeasurement(sensors, maintenance);
                History.update(
                    payload.history && payload.history.length
                        ? payload.history
                        : liveHistory
                );
            }

            updateStatus(payload);

            const apiLed = document.getElementById("apiLed");
            if (apiLed) {
                apiLed.classList.remove("bg-red-500");
                apiLed.classList.add("bg-green-500");
            }

        }

        catch(error){

            console.error(error);

            const apiLed = document.getElementById("apiLed");
            if (apiLed) {
                apiLed.classList.remove("bg-green-500");
                apiLed.classList.add("bg-red-500");
            }

        }

    }

    function appendLiveMeasurement(sensors, maintenance){
        liveHistory.push({
            timestamp: new Date().toLocaleTimeString(),
            temperature: Number(sensors.temperature || 0),
            vibration: Number(sensors.vibration || 0),
            current: Number(sensors.current || 0),
            speed: Number(sensors.speed || 0),
            torque: Number(sensors.torque || 0),
            health: Number(maintenance.health ?? sensors.health ?? 0)
        });

        if(liveHistory.length > MAX_HISTORY){
            liveHistory.shift();
        }
    }

    function updateStatus(payload){
        const simulation = payload.simulation || {};
        const motor = payload.motor || {};
        const simStatus = document.getElementById("simStatus");
        const faultStatus = document.getElementById("faultStatus");
        const motorLed = document.getElementById("motorLed");

        if(simStatus){
            simStatus.innerHTML = simulation.running ? "RUNNING" : "STOPPED";
        }

        if(motorLed){
            motorLed.classList.remove("status-dot-online", "status-dot-offline");
            motorLed.classList.add(motor.running === false ? "status-dot-offline" : "status-dot-online");
        }

        if(faultStatus){
            faultStatus.innerHTML = `Fault: ${simulation.fault || "NORMAL"}`;
        }
    }

    function start(){

        updateDashboard();

        setInterval(updateDashboard,1000);

    }

    return{

        start,
        refresh: updateDashboard

    }

})();

window.DashboardAPI = DashboardAPI;

