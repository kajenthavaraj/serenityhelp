from transformers import pipeline
from fastapi import FastAPI, Request
import uvicorn

from uagents import Agent, Context, Bureau

# Load emotion detection model
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def analyze_text_metrics(text):
    results = emotion_model(text)
    text_lower = text.lower()

    suicide_keywords = ["kill myself", "suicidal", "die", "ending it", "pills", "overdose", "no way out"]
    psychosis_keywords = ["voices", "hallucinate", "not real", "they’re watching me", "i’m not me"]

    metrics = {
        "self_harm": 0,
        "homicidal": 0,
        "distress": 0,
        "psychosis": 0
    }

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

    if any(word in text_lower for word in suicide_keywords):
        metrics["self_harm"] = max(metrics["self_harm"], 0.8)
    if any(word in text_lower for word in psychosis_keywords):
        metrics["psychosis"] = max(metrics["psychosis"], 0.8)

    for k in metrics:
        metrics[k] = round(min(metrics[k] * 100, 100), 2)

    return metrics

# Define uAgent
agent = Agent(name="sentiment_agent")

@agent.on_message()
async def handle_message(ctx: Context, sender: str, msg: str):
    metrics = analyze_text_metrics(msg)
    await ctx.send(sender, str(metrics))

# FastAPI wrapper
app = FastAPI()

@app.post("/")
async def analyze_text(request: Request):
    data = await request.json()
    text = data.get("text", "")
    result = analyze_text_metrics(text)
    return result

# Run both FastAPI and agent
if __name__ == "__main__":
    bureau = Bureau()
    bureau.add(agent)
    bureau.run_in_thread()
    uvicorn.run(app, host="0.0.0.0", port=8000)
