from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("I want to suicide myself, I hate this world!")[0]
print(f"label: {result['label']}, with score: {round(result['score'], 4)}")

