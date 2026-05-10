import pandas as pd

df = pd.read_csv("dataset.csv")

mapping = {
    0: "sad",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

df["emotion"] = df["label"].map(mapping)

df = df[["text", "emotion"]]

df.to_csv("dataset.csv", index=False)

print("Dataset fixed!")
print(df.head())