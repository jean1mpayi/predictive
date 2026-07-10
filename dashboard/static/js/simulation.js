const Simulation = (()=>{

    function init(){

        document
            .getElementById("btnStart")
            .addEventListener("click",start);

        document
            .getElementById("btnStop")
            .addEventListener("click",stop);

        const faultSelector = document.getElementById("faultSelector");
        const faultApplyBtn = document.getElementById("faultApplyBtn");

        if(faultApplyBtn){
            faultApplyBtn.addEventListener("click", applyFault);
        }

        if(faultSelector){
            faultSelector.addEventListener("change", function(){
                applyFault();
            });
        }

    }

    async function start(){

        await fetch("/simulation/start/");

        document
            .getElementById("simLed")
            .classList.replace("bg-red-500","bg-green-500");

        document
            .getElementById("simStatus")
            .innerHTML="RUNNING";

    }

    async function stop(){

        await fetch("/simulation/stop/");

        document
            .getElementById("simLed")
            .classList.replace("bg-green-500","bg-red-500");

        document
            .getElementById("simStatus")
            .innerHTML="STOPPED";

    }

    async function applyFault(){

        const selector = document.getElementById("faultSelector");

        if(!selector){
            return;
        }

        const fault = selector.value;

        const response = await fetch(`/simulation/fault/${fault}/`);
        const data = await response.json();

        document.getElementById("faultStatus").innerHTML =
            `Fault: ${data.fault_mode || fault}`;

        if (typeof DashboardAPI !== "undefined" && DashboardAPI.refresh) {
            DashboardAPI.refresh();
        }

    }

    return{

        init,
        applyFault

    }

})();

window.Simulation = Simulation;
