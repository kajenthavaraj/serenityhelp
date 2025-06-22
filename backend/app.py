from flask import Flask, request

app = Flask(__name__)

@app.route('/vapi-webhook', methods=['POST'])
def handle_webhook():
    data = request.json

    # Handle transcription (user only, direct transcript)
    if data.get("event") == "transcription":
        transcript = data.get("transcript")
        if transcript:
            print(f"User: {transcript}")

    # Handle structured conversation from artifact.messages
    elif data.get("message", {}).get("type") == "speech-update":
        messages = data.get("message", {}).get("artifact", {}).get("messages", [])
        for msg in messages:
            role = msg.get("role")
            content = msg.get("message")
            if role == "user":
                print(f"User: {content}")
            elif role == "bot":
                print(f"Agent: {content}")

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
