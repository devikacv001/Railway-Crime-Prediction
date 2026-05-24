// Elements
const yearInput = document.getElementById('year');
const stateSelect = document.getElementById('state');
const predictBtn = document.getElementById('predictBtn');
const predictionResult = document.getElementById('predictionResult');
const panicBtn = document.getElementById('panicBtn');
const panicResult = document.getElementById('panicResult');
const trendBtn = document.getElementById('trendBtn');
const trendCanvas = document.getElementById('trendChartCanvas').getContext('2d');
let trendChart;

// Predict Arrests
predictBtn.addEventListener('click', async () => {
  const year = yearInput.value;
  const state = stateSelect.value;
  predictionResult.textContent = '';

  if (!year) {
    predictionResult.textContent = 'Please enter a year.';
    return;
  }

  try {
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ year, state })
    });
    const data = await resp.json();
    predictionResult.textContent =
      `Prediction for ${data.state} in ${data.year}: ${data.prediction}`;
  } catch (err) {
    predictionResult.textContent = 'Error fetching prediction.';
    console.error(err);
  }
});

// Trigger Panic
panicBtn.addEventListener('click', async () => {
  panicResult.textContent = '';
  try {
    const resp = await fetch('/panic', { method: 'POST' });
    const data = await resp.json();
    panicResult.textContent = data.message;
  } catch (err) {
    panicResult.textContent = 'Error sending panic alert.';
    console.error(err);
  }
});

// Show Trend
trendBtn.addEventListener('click', async () => {
  const state = stateSelect.value;
  try {
    const resp = await fetch('/trend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state })
    });
    const data = await resp.json();

    // Prepare chart data
    const labels = Object.keys(data.trend);
    const values = Object.values(data.trend);

    if (trendChart) trendChart.destroy();
    trendChart = new Chart(trendCanvas, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: `${data.state} Arrest Trend`,
          data: values,
          borderColor: 'teal',
          fill: false,
          tension: 0.1
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } catch (err) {
    console.error(err);
  }
});