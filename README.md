# EmotiSense AI

An emotion detection web app built with Python, Flask and Machine Learning. Type any text and it tells you what emotion you're feeling.

🔗 Live Demo: https://web-production-3f1bb.up.railway.app


## What it does

- Detects 6 emotions from text: Joy, Sadness, Anger, Fear, Love, Surprise
- Shows confidence score and motivational message
- Dashboard with emotion history and chart
- Voice input and downloadable report

## Built with

- Python & Flask
- scikit-learn — Logistic Regression + TF-IDF
- NLTK for text preprocessing
- HTML, CSS, JavaScript
- Chart.js
- Dataset: HuggingFace dair-ai/emotion (16,000+ rows)
- Accuracy: 89%+

## Run locally

```bash
git clone https://github.com/mahnr/emotisense-ai
cd emotisense-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python download_dataset.py
python train_model.py
python app.py

Open http://localhost:5000

Made by Mahnoor Naseem
⭐ If you like this project, please give it a star!