const Charts = (() => {

    const MAX_POINTS = 100;

    const history = {
        labels: [],
        temperature: [],
        vibration: [],
        current: [],
        speed: [],
        torque: [],
        health: [],
    };

    let currentVariable = "temperature";
    let canvas = null;
    let context = null;

    const colors = {
        temperature: "#ef4444",
        vibration: "#eab308",
        current: "#22c55e",
        speed: "#3b82f6",
        torque: "#8b5cf6",
        health: "#06b6d4",
    };

    const labels = {
        temperature: "Temperature",
        vibration: "Vibration",
        current: "Current",
        speed: "Speed",
        torque: "Torque",
        health: "Health",
    };

    function init() {
        canvas = document.getElementById("mainChart");
        if (!canvas) {
            return;
        }

        context = canvas.getContext("2d");
        resize();
        draw();

        const selector = document.getElementById("chartSelector");
        if (selector) {
            selector.addEventListener("change", function () {
                change(this.value);
            });
        }

        window.addEventListener("resize", resize);
    }

    function resize() {
        if (!canvas || !context) {
            return;
        }

        const parent = canvas.parentElement;
        const width = parent ? parent.clientWidth : canvas.clientWidth;
        const height = parent ? parent.clientHeight : 320;
        const ratio = window.devicePixelRatio || 1;

        canvas.width = Math.max(width * ratio, 300);
        canvas.height = Math.max(height * ratio, 220);
        canvas.style.width = `${Math.max(width, 300)}px`;
        canvas.style.height = `${Math.max(height, 220)}px`;
        context.setTransform(ratio, 0, 0, ratio, 0, 0);
        draw();
    }

    function push(data) {
        const now = new Date();

        history.labels.push(now.toLocaleTimeString());
        history.temperature.push(Number(data.temperature || 0));
        history.vibration.push(Number(data.vibration || 0));
        history.current.push(Number(data.current || 0));
        history.speed.push(Number(data.speed || 0));
        history.torque.push(Number(data.torque || 0));
        history.health.push(Number(data.health || 0));

        if (history.labels.length > MAX_POINTS) {
            history.labels.shift();
            history.temperature.shift();
            history.vibration.shift();
            history.current.shift();
            history.speed.shift();
            history.torque.shift();
            history.health.shift();
        }

        draw();
    }

    function change(variable) {
        currentVariable = variable in history ? variable : "temperature";
        draw();
    }

    function drawGrid(width, height) {
        context.strokeStyle = "#1e293b";
        context.lineWidth = 1;

        for (let i = 0; i <= 5; i += 1) {
            const y = 20 + ((height - 50) / 5) * i;
            context.beginPath();
            context.moveTo(40, y);
            context.lineTo(width - 10, y);
            context.stroke();
        }
    }

    function drawLine(values, width, height) {
        if (!values.length) {
            return;
        }

        const plotWidth = width - 60;
        const plotHeight = height - 50;
        const minValue = Math.min(...values, 0);
        const maxValue = Math.max(...values, 1);
        const range = Math.max(maxValue - minValue, 1);
        const stepX = values.length > 1 ? plotWidth / (values.length - 1) : plotWidth;

        context.strokeStyle = colors[currentVariable];
        context.lineWidth = 3;
        context.beginPath();

        values.forEach((value, index) => {
            const x = 40 + stepX * index;
            const normalized = (value - minValue) / range;
            const y = 20 + plotHeight - normalized * plotHeight;

            if (index === 0) {
                context.moveTo(x, y);
            } else {
                context.lineTo(x, y);
            }
        });

        context.stroke();
    }

    function drawLegend(width) {
        context.fillStyle = "#e2e8f0";
        context.font = "600 14px Inter, sans-serif";
        context.fillText(labels[currentVariable], 44, 18);

        context.fillStyle = colors[currentVariable];
        context.fillRect(width - 140, 8, 10, 10);
        context.fillStyle = "#e2e8f0";
        context.font = "12px Inter, sans-serif";
        context.fillText("Live signal", width - 124, 17);
    }

    function drawEmpty(width, height) {
        context.fillStyle = "#94a3b8";
        context.font = "14px Inter, sans-serif";
        context.fillText("Waiting for live measurements...", 50, height / 2);
    }

    function draw() {
        if (!canvas || !context) {
            return;
        }

        const width = canvas.clientWidth || 900;
        const height = canvas.clientHeight || 320;

        context.clearRect(0, 0, width, height);
        context.fillStyle = "#0f172a";
        context.fillRect(0, 0, width, height);

        drawGrid(width, height);
        drawLegend(width);

        const values = history[currentVariable];
        if (!values.length) {
            drawEmpty(width, height);
            return;
        }

        drawLine(values, width, height);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

    return {
        push,
        change,
        draw,
    };

})();

window.Charts = Charts;
