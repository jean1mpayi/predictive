const History = (() => {

    function update(items){

        const container = document.getElementById("history");
        if(!container){
            return;
        }

        if(!items || items.length === 0){
            container.innerHTML = `<div class="text-slate-400">No measurements yet</div>`;
            return;
        }

        container.innerHTML = items.map(item => `
            <div class="history-row">
                <div class="history-time">${item.timestamp || ""}</div>
                <div class="history-values">
                    <span>T ${Number(item.temperature || 0).toFixed(1)}°C</span>
                    <span>V ${Number(item.vibration || 0).toFixed(3)}g</span>
                    <span>I ${Number(item.current || 0).toFixed(2)}A</span>
                    <span>S ${Number(item.speed || 0).toFixed(1)}rpm</span>
                    <span>Q ${Number(item.torque || 0).toFixed(2)}N.m</span>
                    <span>H ${Number(item.health || 0).toFixed(1)}%</span>
                </div>
            </div>
        `).join("");
    }

    return {
        update
    };

})();

window.History = History;
