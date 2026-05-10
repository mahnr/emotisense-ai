from datasets import load_dataset
import pandas as pd

print("Downloading dataset...")

# Load Hugging Face emotion dataset
dataset = load_dataset("dair-ai/emotion")

# Convert train split into dataframe
df = pd.DataFrame(dataset["train"])

# Save as CSV
df.to_csv("dataset.csv", index=False)

print("Dataset saved as dataset.csv")
print(df.head())