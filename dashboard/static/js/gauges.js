const Gauges = (() => {

    // Pour afficher la tendance ↑ ↓ →
    let previous = {
        health: null,
        temperature: null,
        current: null,
        speed: null,
        vibration: null,
        torque: null
    };

    //--------------------------------------------------
    // Détermine la couleur selon la valeur
    //--------------------------------------------------

    function getColor(type, value){

        switch(type){
            case "health":
                if(value >= 80) return "text-green-500";
                if(value >= 60) return "text-yellow-500";
                return "text-red-500";

            case "temperature":
                if(value < 60) return "text-green-500";
                if(value < 80) return "text-yellow-500";
                return "text-red-500";

            case "vibration":
                if(value < 0.5) return "text-green-500";
                if(value < 1) return "text-yellow-500";
                return "text-red-500";

            case "current":
                if(value < 10) return "text-green-500";
                if(value < 15) return "text-yellow-500";
                return "text-red-500";

            default:
                return "text-cyan-500";
        }

    }

    //--------------------------------------------------
    // Flèche de tendance
    //--------------------------------------------------

    function trend(type, value){
        if(previous[type] === null){
            previous[type] = value;
            return "➜";
        }
        let arrow="➜";
        if(value > previous[type]) arrow="▲";
        if(value < previous[type]) arrow="▼";
        previous[type]=value;
        return arrow;
    }

    //--------------------------------------------------
    // Update KPI card DOM Elements
    //--------------------------------------------------

    function updateCard(type, value) {
        const valEl = document.getElementById(type + "Value");
        const trendEl = document.getElementById(type + "Trend");
        
        if(valEl && trendEl) {
            valEl.innerText = value.toFixed(2);
            
            const newColor = getColor(type, value);
            const currentTrend = trend(type, value);
            
            trendEl.innerText = currentTrend;
            trendEl.className = `flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 text-xs font-medium ${newColor}`;
        }
    }

    //--------------------------------------------------
    // Mise à jour des 6 cartes
    //--------------------------------------------------

    function update(data){
        updateCard("health", data.health);
        updateCard("temperature", data.temperature);
        updateCard("current", data.current);
        updateCard("speed", data.speed);
        updateCard("vibration", data.vibration);
        updateCard("torque", data.torque);
    }

    return{
        update
    };

})();

window.Gauges = Gauges;
