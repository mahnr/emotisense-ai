"use strict";
const $ = id => document.getElementById(id);

const EMOJI_MAP = {
  sadness:  "😢",
  joy:      "😊",
  love:     "❤️",
  anger:    "😠",
  fear:     "😨",
  surprise: "😲",
};

const COLOR_MAP = {
  sadness:  "#6495ED",
  joy:      "#FFD700",
  love:     "#FF6B9D",
  anger:    "#FF4500",
  fear:     "#9370DB",
  surprise: "#FF69B4",
};

$("user-input").addEventListener("input", () => {
  const len = $("user-input").value.length;
  $("char-count").textContent = len + " / 500";
  if (len > 500) $("user-input").value = $("user-input").value.slice(0, 500);
});

async function analyzeEmotion() {
  const text = $("user-input").value.trim();
  if (!text) { shake($("user-input")); return; }
  showLoading(true); hideResult();
  try {
    const res  = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok) { alert(data.error || "Something went wrong."); return; }
    renderResult(data);
  } catch(e) {
    alert("Network error — make sure Flask is running.");
  } finally { showLoading(false); }
}

function renderResult(d) {
  const emoji = EMOJI_MAP[d.primary] || "😐";
  const color = COLOR_MAP[d.primary] || "#A9A9A9";

  $("res-emoji").textContent      = emoji;
  $("res-primary").textContent    = d.primary;
  $("res-confidence").textContent = d.confidence + "% confidence";
  $("res-reasoning").textContent  = d.reasoning;

  const rc = $("result-card");
  rc.classList.remove("hidden");
  rc.style.borderColor = color + "88";

  const bar = $("progress-bar");
  bar.style.width = "0";
  setTimeout(() => bar.style.width = d.confidence + "%", 50);

  typeMessage($("res-message"), d.message);
  window._lastResult = d;
}

function typeMessage(el, msg) {
  el.textContent = ""; let i = 0;
  const t = setInterval(() => {
    el.textContent += msg[i++];
    if (i >= msg.length) clearInterval(t);
  }, 28);
}

function showLoading(on) { $("loading").classList.toggle("hidden", !on); }
function hideResult()    { $("result-card").classList.add("hidden"); }
function clearInput()    { $("user-input").value = ""; $("char-count").textContent = "0 / 500"; hideResult(); }
function shake(el)       { el.style.animation = "none"; el.offsetHeight; el.style.animation = "shake .4s ease"; }

const _s = document.createElement("style");
_s.textContent = `@keyframes shake{0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-8px)}40%,80%{transform:translateX(8px)}}`;
document.head.appendChild(_s);


function showSection(name) {
  ["home", "analyzer", "dashboard"].forEach(s => {
    $("section-"+s).classList.toggle("active", s===name);
    $("section-"+s).classList.toggle("hidden",  s!==name);
    $("nav-"+s).classList.toggle("active", s===name);
  });
  if (name === "dashboard") setTimeout(loadDashboard, 100);
}

async function loadDashboard() {
  const hist = await fetch("/history").then(r => r.json());
  $("stat-total").textContent = hist.length;
  if (!hist.length) {
    $("stat-top").textContent = "—";
    $("stat-avg").textContent = "—";
    $("history-list").innerHTML = "<p style='color:var(--muted)'>No analyses yet.</p>";
    renderChart({});
    return;
  }
  const freq = {};
  hist.forEach(h => freq[h.primary] = (freq[h.primary]||0)+1);
  $("stat-top").textContent = Object.entries(freq).sort((a,b)=>b[1]-a[1])[0][0];
  $("stat-avg").textContent = (hist.reduce((s,h)=>s+h.confidence,0)/hist.length).toFixed(1)+"%";

  $("history-list").innerHTML = hist.slice(-8).reverse().map(h => `
    <div class="history-item">
      <span class="hist-emoji">${EMOJI_MAP[h.primary] || "😐"}</span>
      <div class="hist-body">
        <p>${h.primary} — ${h.confidence}%</p>
        <small>${h.original.slice(0,60)}${h.original.length>60?"…":""}</small>
        <small style="display:block;margin-top:2px">${h.timestamp}</small>
      </div>
    </div>
  `).join("");
  renderChart(freq);
}

async function clearHistory() {
  await fetch("/clear", { method:"POST" });
  loadDashboard();
}

function downloadReport() {
  const d = window._lastResult; if (!d) return;
  const emoji = EMOJI_MAP[d.primary] || "😐";
  const txt = [
    "EmotiSense AI — Emotion Report",
    "=".repeat(40),
    "Timestamp:  " + d.timestamp,
    "Input:      " + d.original,
    "",
    "Emotion:    " + d.primary + " " + emoji,
    "Confidence: " + d.confidence + "%",
    "", "Message:", d.message,
    "", "Reasoning:", d.reasoning,
  ].join("\n");
  const a = document.createElement("a");
  a.href = "data:text/plain;charset=utf-8," + encodeURIComponent(txt);
  a.download = "emotion_report_" + d.id + ".txt";
  a.click();
}

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const recog = new (window.SpeechRecognition||window.webkitSpeechRecognition)();
  recog.lang = "en-US";
  recog.onresult = e => {
    $("user-input").value = e.results[0][0].transcript;
    $("char-count").textContent = $("user-input").value.length + " / 500";
  };
  $("voice-btn").onclick = () => recog.start();
}