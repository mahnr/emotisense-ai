# ============================================================
# model_training.py — Train & Save Emotion Detection Model
# ============================================================
import pandas as pd, pickle, os, re
import nltk
nltk.download("stopwords", quiet=True)
nltk.download("wordnet",   quiet=True)
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

lemmatizer = WordNetLemmatizer()
stop_words  = set(stopwords.words("english"))

def preprocess(text):
    text   = str(text).lower()
    text   = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = [lemmatizer.lemmatize(t) for t in text.split() if t not in stop_words]
    return " ".join(tokens)

print("Loading dataset...")
df = pd.read_csv("dataset.csv")
print(df["emotion"].value_counts())

df["clean"] = df["text"].apply(preprocess)
df.dropna(inplace=True)

X_train, X_test, y_train, y_test = train_test_split(
    df["clean"], df["emotion"],
    test_size=0.2, random_state=42, stratify=df["emotion"]
)

print("\nVectorizing...")
# Better: ngram (1,3) aur zyada features
vec = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1, 3),       # 1,2,3 word combinations
    sublinear_tf=True,        # log scaling — better accuracy
    min_df=2,
)
X_tr = vec.fit_transform(X_train)
X_te = vec.transform(X_test)

# Class weights — balanced training (important!)
classes = np.unique(y_train)
weights = compute_class_weight("balanced", classes=classes, y=y_train)
class_weight_dict = dict(zip(classes, weights))
print("\nClass weights:", class_weight_dict)

print("Training model...")
clf = LogisticRegression(
    max_iter=1000,
    C=10,                          # better regularization
    solver="lbfgs",
    multi_class="auto",
    class_weight=class_weight_dict  # balanced classes
)
clf.fit(X_tr, y_train)

y_pred = clf.predict(X_te)
acc    = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc*100:.2f}%")
print(classification_report(y_test, y_pred))

os.makedirs("model", exist_ok=True)
pickle.dump(clf, open("model/emotion_model.pkl", "wb"))
pickle.dump(vec, open("model/vectorizer.pkl",    "wb"))
print("\nModel saved! Ab app.py restart karo.")