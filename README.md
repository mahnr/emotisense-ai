<<<<<<< HEAD
# 🧠 EmotiSense AI — Emotion Detection System

AI-powered web app that detects 12 emotions from text using NLP + ML.

## 🚀 Quick Start

```bash
# 1. Clone & enter project
git clone https://github.com/yourname/emotion-detector
cd emotion-detector

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# 5. Train the model (uses dataset.csv)
python model_training.py

# 6. Run the Flask app
python app.py
```

Open http://localhost:5000 in your browser.

## 📁 Structure
emotion-detector/
├── app.py               Flask backend
├── model_training.py    ML training script
├── dataset.csv          Training data
├── requirements.txt
├── templates/index.html Frontend
├── static/
│   ├── style.css
│   ├── script.js
│   └── charts.js
└── model/
    ├── emotion_model.pkl
    └── vectorizer.pkl

## 🎯 Emotions Detected
Happy 😊 • Sad 😢 • Angry 😠 • Fearful 😨 • Surprised 😲
Loving ❤️ • Excited 🤩 • Anxious 😰 • Confused 😕
Lonely 😔 • Motivated 💪 • Neutral 😐

## 💡 Getting a Better Dataset
Replace dataset.csv with:
- Kaggle: "Emotions" by dair-ai (~20 000 rows)
- HuggingFace: datasets.load_dataset("emotion")
- GoEmotions by Google Research

## 🔑 Tech Stack
Python · Flask · scikit-learn · NLTK · TF-IDF · Chart.js
=======
# emotisense-ai
AI-Powered Emotion Detection System using NLP and Flask
>>>>>>> 889c7cfa7879ee2acc96bf2e5fee4a42e101033b
