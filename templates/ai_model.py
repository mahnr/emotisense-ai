from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def detect_emotion(text):
    results = classifier(text)[0]

    
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    top = results[0]

    return {
        "emotion": top["label"],
        "confidence": round(top["score"] * 100, 1),
        "all": results
    }