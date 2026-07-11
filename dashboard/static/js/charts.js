const Charts = (() => {
  const MAX_POINTS = 50; // Ajusté pour un rendu visuel aéré comme sur l'image

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

  // Palette "Dark Neon"
  const styleConfig = {
    bg: "#0f172a", // Fond slate-900 (pour correspondre au HTML)
    grid: "rgba(255, 255, 255, 0.12)", // Grille subtile
    text: "#cbd5e1", // Texte clair
    gradientBottom: "rgba(15, 23, 42, 0.0)", // Transparent
  };

  // Couleurs dynamiques selon la variable sélectionnée
  const dynamicColors = {
    temperature: { line: "#fb7185", glow: "rgba(251, 113, 133, 0.6)" }, // Rose
    vibration: { line: "#fbbf24", glow: "rgba(251, 191, 36, 0.6)" }, // Amber
    current: { line: "#34d399", glow: "rgba(52, 211, 153, 0.6)" }, // Menthe
    speed: { line: "#60a5fa", glow: "rgba(96, 165, 250, 0.6)" }, // Bleu
    torque: { line: "#a78bfa", glow: "rgba(167, 139, 250, 0.6)" }, // Violet
    health: { line: "#22d3ee", glow: "rgba(34, 211, 238, 0.6)" }, // Cyan
  };

  const labels = {
    temperature: "Température (°C)",
    vibration: "Vibration (mm/s)",
    current: "Courant (A)",
    speed: "Vitesse (RPM)",
    torque: "Couple (Nm)",
    health: "Santé (%)",
  };

  // Marges pour l'encadrement de la grille et les libellés
  const padding = { top: 35, right: 30, bottom: 45, left: 55 };

  function init() {
    canvas = document.getElementById("mainChart");
    if (!canvas) return;

    context = canvas.getContext("2d");
    resize();

    const selector = document.getElementById("chartSelector");
    if (selector) {
      selector.addEventListener("change", function () {
        change(this.value);
      });
    }

    window.addEventListener("resize", resize);
  }

  function resize() {
    if (!canvas || !context) return;

    const parent = canvas.parentElement;
    const width = parent ? parent.clientWidth : 700;
    const height = parent ? parent.clientHeight : 350;
    const ratio = window.devicePixelRatio || 1;

    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;

    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw();
  }

  function push(data) {
    const now = new Date();
    history.labels.push(now.getTime());
    history.temperature.push(Number(data.temperature || 0));
    history.vibration.push(Number(data.vibration || 0));
    history.current.push(Number(data.current || 0));
    history.speed.push(Number(data.speed || 0));
    history.torque.push(Number(data.torque || 0));
    history.health.push(Number(data.health || 0));

    if (history.labels.length > MAX_POINTS) {
      Object.keys(history).forEach((key) => history[key].shift());
    }

    draw();
  }

  function change(variable) {
    currentVariable = variable in history ? variable : "temperature";
    draw();
  }

  function getScales(values, width, height) {
    const plotWidth = width - padding.left - padding.right;
    const plotHeight = height - padding.top - padding.bottom;

    const minVal = Math.min(...values, 0);
    const maxVal = Math.max(...values, 10);
    const padY = (maxVal - minVal) * 0.15 || 5;

    return {
      minY: Math.floor(minVal),
      maxY: Math.ceil(maxVal + padY),
      plotWidth,
      plotHeight,
    };
  }

  function drawGridAndAxes(width, height, minY, maxY, plotWidth, plotHeight) {
    context.strokeStyle = styleConfig.grid;
    context.lineWidth = 1;
    context.fillStyle = styleConfig.text;
    context.font = "600 11px 'Inter', sans-serif";
    context.textBaseline = "middle";

    const gridRows = 5;
    const gridCols = 8;

    // 1. Lignes horizontales + Libellés Y (Gauche)
    context.textAlign = "right";
    for (let i = 0; i <= gridRows; i++) {
      const ratio = i / gridRows;
      const y = padding.top + plotHeight * (1 - ratio);
      const val = minY + (maxY - minY) * ratio;

      context.beginPath();
      context.moveTo(padding.left, y);
      context.lineTo(width - padding.right, y);
      context.stroke();

      context.fillText(Math.round(val), padding.left - 12, y);
    }

    // 2. Lignes verticales + Libellés X (Bas en secondes)
    context.textAlign = "center";
    context.textBaseline = "top";
    for (let i = 0; i <= gridCols; i++) {
      const ratio = i / gridCols;
      const x = padding.left + plotWidth * ratio;

      context.beginPath();
      context.moveTo(x, padding.top);
      context.lineTo(x, padding.top + plotHeight);
      context.stroke();

      const secAgo = Math.round((1 - ratio) * 20);
      const labelX = secAgo === 0 ? "MAINTENANT" : `-${secAgo}s`;
      context.fillText(labelX, x, padding.top + plotHeight + 14);
    }

    // 3. Encadrement extérieur de la grille (Box)
    context.strokeStyle = "rgba(255, 255, 255, 0.25)";
    context.strokeRect(padding.left, padding.top, plotWidth, plotHeight);
  }

  // Générateur de courbe lissée (Catmull-Rom vers Bézier)
  function traceSmoothPath(points) {
    context.beginPath();
    context.moveTo(points[0].x, points[0].y);

    const tension = 0.3;
    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[i === 0 ? i : i - 1];
      const p1 = points[i];
      const p2 = points[i + 1];
      const p3 = points[i + 2 < points.length ? i + 2 : i + 1];

      const cp1x = p1.x + (p2.x - p0.x) * tension;
      const cp1y = p1.y + (p2.y - p0.y) * tension;
      const cp2x = p2.x - (p3.x - p1.x) * tension;
      const cp2y = p2.y - (p3.y - p1.y) * tension;

      context.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, p2.x, p2.y);
    }
  }

  function drawLineAndArea(values, plotWidth, plotHeight, minY, maxY) {
    if (values.length < 2) return;

    const stepX = plotWidth / (values.length - 1);
    const rangeY = maxY - minY || 1;

    const points = values.map((val, idx) => ({
      x: padding.left + stepX * idx,
      y: padding.top + plotHeight - ((val - minY) / rangeY) * plotHeight,
      val: val,
    }));

    // 1. Dégradé sous la courbe (Area)
    const activeColor = dynamicColors[currentVariable];
    const gradient = context.createLinearGradient(
      0,
      padding.top,
      0,
      padding.top + plotHeight,
    );
    gradient.addColorStop(0, activeColor.glow);
    gradient.addColorStop(1, styleConfig.gradientBottom);

    traceSmoothPath(points);
    context.lineTo(points[points.length - 1].x, padding.top + plotHeight);
    context.lineTo(points[0].x, padding.top + plotHeight);
    context.closePath();
    context.fillStyle = gradient;
    context.fill();

    // 2. Trait principal
    traceSmoothPath(points);
    context.strokeStyle = activeColor.line;
    context.lineWidth = 3.5;
    context.lineJoin = "round";
    context.lineCap = "round";
    context.shadowColor = activeColor.glow;
    context.shadowBlur = 10;
    context.stroke();
    context.shadowBlur = 0; // Reset ombre

    // 3. Dessin du marqueur de Pic (Badge sur la valeur maximale)
    let maxPoint = points[0];
    points.forEach((p) => {
      if (p.val > maxPoint.val) maxPoint = p;
    });

    drawPeakMarker(maxPoint.x, maxPoint.y);
  }

  function drawPeakMarker(x, y) {
    const activeColor = dynamicColors[currentVariable];

    // Halo extérieur
    context.beginPath();
    context.arc(x, y, 14, 0, Math.PI * 2);
    context.fillStyle = activeColor.glow;
    context.fill();

    // Cercle intermédiaire
    context.beginPath();
    context.arc(x, y, 8, 0, Math.PI * 2);
    context.fillStyle = activeColor.line;
    context.fill();

    // Point central blanc
    context.beginPath();
    context.arc(x, y, 3.5, 0, Math.PI * 2);
    context.fillStyle = "#ffffff";
    context.fill();
  }

  function drawEmpty(width, height) {
    context.fillStyle = "#8b5cf6";
    context.font = "14px Inter, sans-serif";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(
      "En attente de la télémétrie en temps réel...",
      width / 2,
      height / 2,
    );
  }

  function draw() {
    if (!canvas || !context) return;

    const width = canvas.width / (window.devicePixelRatio || 1);
    const height = canvas.height / (window.devicePixelRatio || 1);

    // Fond global sombre
    context.fillStyle = styleConfig.bg;
    context.fillRect(0, 0, width, height);

    const values = history[currentVariable];
    if (!values || !values.length) {
      drawEmpty(width, height);
      return;
    }

    const scales = getScales(values, width, height);
    drawGridAndAxes(
      width,
      height,
      scales.minY,
      scales.maxY,
      scales.plotWidth,
      scales.plotHeight,
    );
    drawLineAndArea(
      values,
      scales.plotWidth,
      scales.plotHeight,
      scales.minY,
      scales.maxY,
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  return { push, change, draw };
})();

window.Charts = Charts;
