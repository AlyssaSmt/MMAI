// ======================
// Wörter (MÜSSEN Klassen des Modells sein!)
// ======================
const WORDS = [
  "cat",
  "cup",
  "car",
  "sun",
  "eye",
  "house",
  "pants",
  "tree",
  "strawberry",
  "wine glass"
];

let targetWord = null;

// ======================
// DOM-Elemente
// ======================
const targetWordSpan = document.getElementById("target-word");

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const clearBtn = document.getElementById("clear");
const predictBtn = document.getElementById("predict");

const predictionSpan = document.getElementById("prediction");
const confidenceSpan = document.getElementById("confidence");
const topList = document.getElementById("top-list");

// ======================
// Canvas Setup (WICHTIG!)
// ======================
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.lineWidth = 12;
ctx.lineCap = "round";
ctx.strokeStyle = "black";

let drawing = false;

// ======================
// Zielwort wählen
// ======================
function chooseNewWord() {
  const i = Math.floor(Math.random() * WORDS.length);
  targetWord = WORDS[i];
  targetWordSpan.textContent = targetWord;
}

// direkt beim Start
chooseNewWord();

// ======================
// Events
// ======================
canvas.addEventListener("mousedown", () => {
  drawing = true;
  ctx.beginPath();
});

canvas.addEventListener("mouseup", () => {
  drawing = false;
  ctx.beginPath();
  maybePredict();
});

canvas.addEventListener("mouseleave", () => {
  drawing = false;
});

canvas.addEventListener("mousemove", draw);

clearBtn.addEventListener("click", () => {
  // Canvas leeren + weiß füllen
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.beginPath();
  predictionSpan.textContent = "–";
  confidenceSpan.textContent = "–";
  topList.innerHTML = "";

  // Neues Wort für nächste Runde
  chooseNewWord();
});

predictBtn.addEventListener("click", maybePredict);

// ======================
// Zeichnen
// ======================
function draw(e) {
  if (!drawing) return;

  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
}

// ======================
// Ink-Menge prüfen
// ======================
function getInkAmount() {
  const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
  let count = 0;
  for (let i = 0; i < data.length; i += 4) {
    if (data[i] < 250) count++;
  }
  return count;
}

// ======================
// Prediction
// ======================
async function maybePredict() {
  const ink = getInkAmount();
  if (ink < 1500) {
    predictionSpan.textContent = "🤔 noch zu wenig gezeichnet";
    confidenceSpan.textContent = "";
    topList.innerHTML = "";
    return;
  }

  try {
    const dataUrl = canvas.toDataURL("image/png");
    const formData = new FormData();
    formData.append("image_base64", dataUrl);

    const response = await fetch("http://127.0.0.1:8001/predict", {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    updateUI(result);

  } catch (err) {
    predictionSpan.textContent = "⚠️ Server nicht erreichbar";
    console.error(err);
  }
}

// ======================
// UI + Montagsmaler-Logik
// ======================
function updateUI(result) {
  const conf = Number(result.confidence);
  const prediction = result.prediction;

  let status = "";

  if (prediction === targetWord && conf >= 0.35) {
    status = "✅ richtig!";
  } else if (conf < 0.25) {
    status = "🤔 unsicher";
  } else {
    status = "❌ falsch";
  }

  predictionSpan.textContent = `${prediction} ${status}`;
  confidenceSpan.textContent = Math.round(conf * 100) + "%";

  // Top-3 anzeigen
  topList.innerHTML = "";
  (result.top || []).forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.label}: ${Math.round(item.confidence * 100)}%`;
    topList.appendChild(li);
  });
}
