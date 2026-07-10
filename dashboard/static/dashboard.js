const tempData = [];
const vibData = [];
const currentData = [];
const healthData = [];
const labels = [];

// ======================
// CHARTS
// ======================
const tempChart = new Chart(document.getElementById("tempChart"), {
  type: "line",
  data: {
    labels: labels,
    datasets: [
      {
        label: "Température",
        data: tempData,
        borderColor: "red",
      },
    ],
  },
});

const vibChart = new Chart(document.getElementById("vibChart"), {
  type: "line",
  data: {
    labels: labels,
    datasets: [
      {
        label: "Vibration",
        data: vibData,
        borderColor: "blue",
      },
    ],
  },
});

const currentChart = new Chart(document.getElementById("currentChart"), {
  type: "line",
  data: {
    labels: labels,
    datasets: [
      {
        label: "Courant",
        data: currentData,
        borderColor: "green",
      },
    ],
  },
});

const healthChart = new Chart(document.getElementById("healthChart"), {
  type: "line",
  data: {
    labels: labels,
    datasets: [
      {
        label: "Health",
        data: healthData,
        borderColor: "orange",
      },
    ],
  },
});

// ======================
// LOOP TEMPS RÉEL
// ======================
async function fetchData() {
  const res = await fetch("/api/latest/");
  const data = await res.json();

  const time = new Date().toLocaleTimeString();

  labels.push(time);

  tempData.push(data.temperature);
  vibData.push(data.vibration);
  currentData.push(data.current);
  healthData.push(data.health);

  // limiter taille (anti crash)
  if (labels.length > 20) {
    labels.shift();
    tempData.shift();
    vibData.shift();
    currentData.shift();
    healthData.shift();
  }

  tempChart.update();
  vibChart.update();
  currentChart.update();
  healthChart.update();
}

// update chaque seconde
setInterval(fetchData, 1000);
