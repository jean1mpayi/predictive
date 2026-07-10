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

                if(value >= 80) return "text-green-400";
                if(value >= 60) return "text-yellow-400";
                return "text-red-400";

            case "temperature":

                if(value < 60) return "text-green-400";
                if(value < 80) return "text-yellow-400";
                return "text-red-400";

            case "vibration":

                if(value < 0.5) return "text-green-400";
                if(value < 1) return "text-yellow-400";
                return "text-red-400";

            case "current":

                if(value < 10) return "text-green-400";
                if(value < 15) return "text-yellow-400";
                return "text-red-400";

            default:

                return "text-cyan-400";

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
    // Création d'une carte KPI (Tailwind)
    //--------------------------------------------------

    function card(icon, title, value, unit, type){

        // Accent definitions per type (left bar color + glow + icon color)
        const accent = {
            health:      { bar: "bg-cyan-400",   glow: "shadow-[0_0_18px_rgba(34,211,238,0.35)]",  icon: "text-cyan-400"   },
            temperature: { bar: "bg-amber-400",  glow: "shadow-[0_0_18px_rgba(245,158,11,0.35)]",  icon: "text-amber-400"  },
            current:     { bar: "bg-green-400",  glow: "shadow-[0_0_18px_rgba(74,222,128,0.35)]",  icon: "text-green-400"  },
            speed:       { bar: "bg-blue-400",   glow: "shadow-[0_0_18px_rgba(96,165,250,0.35)]",  icon: "text-blue-400"   },
            vibration:   { bar: "bg-rose-400",   glow: "shadow-[0_0_18px_rgba(251,113,133,0.35)]", icon: "text-rose-400"   },
            torque:      { bar: "bg-purple-400", glow: "shadow-[0_0_18px_rgba(192,132,252,0.35)]", icon: "text-purple-400" }
        }[type] || { bar: "bg-cyan-400", glow: "shadow-[0_0_18px_rgba(34,211,238,0.35)]", icon: "text-cyan-400" };

        const valueColor = getColor(type, value);

        return `
        <div class="relative overflow-hidden rounded-[1.15rem] border border-slate-400/15 bg-gradient-to-b from-slate-900/98 to-slate-950/98 shadow-[0_18px_40px_rgba(0,0,0,0.26),inset_0_1px_0_rgba(255,255,255,0.03)] p-4 h-full">
            <span class="absolute inset-y-0 left-0 w-[0.35rem] ${accent.bar} ${accent.glow}"></span>
            <div class="flex items-center justify-between gap-3 mb-4">
                <div class="w-[2.8rem] h-[2.8rem] rounded-[0.95rem] grid place-items-center bg-slate-900/88 border border-slate-400/15 ${accent.icon} text-[1.35rem]">${icon}</div>
                <span class="text-[0.95rem] ${valueColor}">${trend(type, value)}</span>
            </div>
            <p class="m-0 text-slate-400 text-[0.76rem] uppercase tracking-[0.16em]">${title}</p>
            <h2 class="mt-1 text-slate-50 text-[clamp(1.55rem,2.2vw,2rem)] leading-none font-black ${valueColor}">${value.toFixed(2)}</h2>
            <p class="mt-1 text-slate-400 text-[0.82rem]">${unit}</p>
        </div>
        `;

    }

    //--------------------------------------------------
    // Mise à jour des 6 cartes
    //--------------------------------------------------

    function update(data){

        document.getElementById("healthCard").innerHTML=

            card(
                "❤️",
                "Health",
                data.health,
                "%",
                "health"
            );

        document.getElementById("temperatureCard").innerHTML=

            card(
                "🌡",
                "Temperature",
                data.temperature,
                "°C",
                "temperature"
            );

        document.getElementById("currentCard").innerHTML=

            card(
                "⚡",
                "Current",
                data.current,
                "A",
                "current"
            );

        document.getElementById("speedCard").innerHTML=

            card(
                "🌀",
                "Speed",
                data.speed,
                "rpm",
                "speed"
            );

        document.getElementById("vibrationCard").innerHTML=

            card(
                "📈",
                "Vibration",
                data.vibration,
                "g",
                "vibration"
            );

        document.getElementById("torqueCard").innerHTML=

            card(
                "⚙",
                "Torque",
                data.torque,
                "N.m",
                "torque"
            );

    }

    return{

        update

    };

})();

window.Gauges = Gauges;
