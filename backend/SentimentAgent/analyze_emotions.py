from transformers import pipeline

# Load emotion detection pipeline
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def analyze_text_metrics(text):
    results = emotion_model(text)

    # Lowercase text for keyword checks
    text_lower = text.lower()

    # Keyword-based override logic
    suicide_keywords = ["kill myself", "suicidal", "die", "ending it", "pills", "overdose", "no way out"]
    psychosis_keywords = ["voices", "hallucinate", "not real", "they’re watching me", "i’m not me"]

    metrics = {
        "self_harm": 0,
        "homicidal": 0,
        "distress": 0,
        "psychosis": 0
    }

    # Add emotion model scores
    for result in results:
        label = result['label']
        score = result['score']

        if label == 'sadness':
            metrics["self_harm"] += score
            metrics["distress"] += score * 0.6
        elif label in ['anger', 'fear']:
            metrics["homicidal"] += score
            metrics["distress"] += score * 0.5
        elif label == 'joy':
            metrics["psychosis"] += score * 0.3
        elif label == 'surprise':
            metrics["psychosis"] += score * 0.5

    # Keyword boosts
    if any(word in text_lower for word in suicide_keywords):
        metrics["self_harm"] = max(metrics["self_harm"], 0.8)  # Force to at least 80%
    if any(word in text_lower for word in psychosis_keywords):
        metrics["psychosis"] = max(metrics["psychosis"], 0.8)

    # Final clean up
    for k in metrics:
        metrics[k] = round(min(metrics[k] * 100, 100), 2)

    return metrics


# For testing from command line
if __name__ == "__main__":
    while True:
        text = input("\nEnter text to analyze (or 'q' to quit): ")
        if text.lower() == 'q':
            break
        result = analyze_text_metrics(text)
        print("Mental Health Risk Metrics:", result)
