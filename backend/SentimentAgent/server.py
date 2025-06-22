from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'frontend.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.json.get('text', '')
    print(f"Received text for analysis: {text}")

    # Simulated response
    return jsonify({
        "crisis_risk": 80,
        "distress_level": 75,
        "emotional_intensity": 85,
        "tonality_risk": 70,
        "urgency": "high",
        "recommendation": "Immediate intervention recommended",
        "key_indicators": ["hopeless", "overwhelmed", "death", "pills"],
        "confidence": 0.92,
        "next_check_seconds": 30
    })

@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    audio_file = request.files.get('audio')
    text = request.form.get('text', '')
    print(f"Received audio and text for analysis: {text}, {audio_file}")

    # Simulated response
    return jsonify({
        "crisis_risk": 55,
        "distress_level": 48,
        "emotional_intensity": 70,
        "tonality_risk": 63,
        "urgency": "high",
        "recommendation": "Escalate to supervisor for immediate review",
        "key_indicators": ["shaky_voice", "fast_speech"],
        "confidence": 0.91,
        "next_check_seconds": 30
    })

if __name__ == '__main__':
    app.run(debug=True)
