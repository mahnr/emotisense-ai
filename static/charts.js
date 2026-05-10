/* ============================================================
   charts.js — Chart.js Emotion Distribution Chart
   ============================================================ */
// ═══════════════════════════════════════════
// CHANGE 1: static/charts.js
// Chart chhota karo — height kam karo
// ═══════════════════════════════════════════

let emotionChart = null;

function renderChart(freq) {
  const labels = Object.keys(freq);
  const values = Object.values(freq);
  const colors = ["#7c3aed","#3b82f6","#f59e0b","#ef4444","#10b981","#ec4899"];
  const ctx = document.getElementById("emotionChart").getContext("2d");
  if (emotionChart) emotionChart.destroy();

  if (!labels.length) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = "#94a3b8";
    ctx.font = "14px Segoe UI";
    ctx.textAlign = "center";
    ctx.fillText("No data yet!", ctx.canvas.width / 2, 60);
    return;
  }

  emotionChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, labels.length),
        borderColor: "#0a0a14",
        borderWidth: 3,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      cutout: "55%",   /* ← mota ring */
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#e2e8f0",
            padding: 10,
            font: { size: 16 },
            boxWidth: 16,
            padding: 20,
          }
        },
        tooltip: {
          callbacks: {
            label: c => ` ${c.label}: ${c.parsed} time(s)`
          }
        }
      }
    }
  });
}