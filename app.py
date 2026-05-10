# ============================================================
# app.py — Flask Backend for Emotion Detection App
# ============================================================
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import pickle, os, re, uuid
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download("stopwords", quiet=True)
nltk.download("wordnet",   quiet=True)

app = Flask(__name__)
app.secret_key = "emotisense-fixed-key"
CORS(app)

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "emotion_model.pkl")
VEC_PATH   = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(VEC_PATH, "rb") as f:
    vectorizer = pickle.load(f)


print("Model classes:", model.classes_)

EMOTION_META = {
    "sadness":  {"emoji": "😢", "color": "#6495ED"},
    "joy":      {"emoji": "😊", "color": "#FFD700"},
    "love":     {"emoji": "❤️",  "color": "#FF6B9D"},
    "anger":    {"emoji": "😠", "color": "#FF4500"},
    "fear":     {"emoji": "😨", "color": "#9370DB"},
    "surprise": {"emoji": "😲", "color": "#FF69B4"},
}

MESSAGES = {
    "sadness":  "It's okay to feel down. Every storm runs out of rain. 🌈 You've got this.",
    "joy":      "Keep spreading that joy! 🌟 Your positive energy is contagious.",
    "love":     "Love is the most powerful force in the universe. Keep sharing it. ❤️",
    "anger":    "Take a deep breath. 🧘 Channel that energy into something powerful.",
    "fear":     "Courage is not the absence of fear — it's acting despite it. 🦁",
    "surprise": "Life is full of surprises! Embrace the unexpected. 🎉",
}

lemmatizer = WordNetLemmatizer()
stop_words  = set(stopwords.words("english"))

def preprocess(text):
    text   = text.lower()
    text   = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = [lemmatizer.lemmatize(t) for t in text.split() if t not in stop_words]
    return " ".join(tokens)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:      return jsonify({"error": "Kuch likho pehle!"}), 400
    if len(text) < 3: return jsonify({"error": "Thoda zyada likho 😊."}), 400

    processed = preprocess(text)
    vec       = vectorizer.transform([processed])
    primary   = model.predict(vec)[0]
    proba     = model.predict_proba(vec)[0]
    classes   = model.classes_
    conf      = round(float(max(proba)) * 100, 1)

    # Top 2 emotions dhundo
    sorted_idx = proba.argsort()[::-1]
    secondary  = classes[sorted_idx[1]]

    # Debug: terminal mein print karo
    print(f"\nText: {text}")
    print(f"Processed: {processed}")
    print(f"Primary: {primary} ({conf}%)")
    print(f"Secondary: {secondary}")
    print(f"All probs: { {c: round(float(p)*100,1) for c, p in zip(classes, proba)} }")

    meta    = EMOTION_META.get(primary, {"emoji": "😊", "color": "#A9A9A9"})
    message = MESSAGES.get(primary, "Keep going! Stay confident...fake it till you make it 😌💫")

    result = {
        "id":         str(uuid.uuid4())[:8],
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "primary":    primary,
        "secondary":  secondary,
        "confidence": conf,
        "emoji":      meta["emoji"],
        "color":      meta["color"],
        "message":    message,
        "reasoning":  f"Analyzed {len(text.split())} word(s). Detected '{primary}' with {conf}% confidence. Secondary: '{secondary}'.",
        "original":   text,
    }

    if "history" not in session:
        session["history"] = []
    session["history"].append(result)
    session.modified = True
    return jsonify(result)

@app.route("/history")
def history():
    return jsonify(session.get("history", []))

@app.route("/clear", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)