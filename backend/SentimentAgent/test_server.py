#!/usr/bin/env python3
"""
Simple test server for frontend sentiment analysis requests
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
import json
import librosa
import numpy as np
from sentiment_service import (
    LiveSentimentRequest, LiveTranscriptSegment, TonalityData,
    live_sentiment_analyzer
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_file('frontend.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Handle sentiment analysis requests"""
    try:
        data = request.get_json()
        
        # Extract text
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Create transcript segment
        segment = LiveTranscriptSegment(
            text=text,
            timestamp=datetime.utcnow().timestamp(),
            confidence=0.9,
            is_final=True
        )
        
        # Handle audio features if provided
        tonality = None
        if 'audio_features' in data:
            features = data['audio_features']
            tonality = TonalityData(
                pitch_mean=features.get('pitch_mean', 0.0),
                pitch_variance=features.get('pitch_variance', 0.0),
                speech_rate=features.get('speech_rate', 0.0),
                volume_level=features.get('volume_level', 0.0),
                voice_tremor=features.get('voice_tremor', 0.0),
                pause_frequency=features.get('pause_frequency', 0.0),
                emotional_tone=features.get('emotional_tone', 'neutral'),
                tone_confidence=features.get('tone_confidence', 0.0)
            )
        
        # Create analysis request
        request_obj = LiveSentimentRequest(
            call_id=f"frontend_test_{datetime.utcnow().timestamp()}",
            transcript_segments=[segment],
            tonality_data=tonality,
            session_duration=0,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Perform analysis
        result = live_sentiment_analyzer.analyze_live_sentiment(request_obj)
        
        # Return results
        return jsonify({
            'crisis_risk': result.crisis_risk,
            'distress_level': result.distress_level,
            'emotional_intensity': result.emotional_intensity,
            'tonality_risk': result.tonality_risk,
            'urgency': result.urgency,
            'recommendation': result.recommendation,
            'key_indicators': result.key_indicators,
            'tone_indicators': result.tone_indicators,
            'confidence': result.confidence,
            'next_check_seconds': result.next_check_seconds,
            'escalation_trigger': result.escalation_trigger,
            'risk_trend': result.risk_trend,
            'analysis_timestamp': result.analysis_timestamp
        })
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    """Handle audio file analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        text = request.form.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Save audio file temporarily
        temp_path = f"/tmp/temp_audio_{datetime.utcnow().timestamp()}.wav"
        audio_file.save(temp_path)
        
        try:
            # Extract audio features using librosa
            audio_features = extract_audio_features(temp_path)
            
            # Clean up temp file
            os.remove(temp_path)
            
            # Create analysis request
            segment = LiveTranscriptSegment(
                text=text,
                timestamp=datetime.utcnow().timestamp(),
                confidence=0.9,
                is_final=True
            )
            
            tonality = TonalityData(**audio_features)
            
            request_obj = LiveSentimentRequest(
                call_id=f"frontend_audio_{datetime.utcnow().timestamp()}",
                transcript_segments=[segment],
                tonality_data=tonality,
                session_duration=0,
                timestamp=datetime.utcnow().isoformat()
            )
            
            # Perform analysis
            result = live_sentiment_analyzer.analyze_live_sentiment(request_obj)
            
            return jsonify({
                'crisis_risk': result.crisis_risk,
                'distress_level': result.distress_level,
                'emotional_intensity': result.emotional_intensity,
                'tonality_risk': result.tonality_risk,
                'urgency': result.urgency,
                'recommendation': result.recommendation,
                'key_indicators': result.key_indicators,
                'tone_indicators': result.tone_indicators,
                'confidence': result.confidence,
                'next_check_seconds': result.next_check_seconds,
                'escalation_trigger': result.escalation_trigger,
                'audio_features': audio_features
            })
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
            
    except Exception as e:
        print(f"Audio analysis error: {str(e)}")
        return jsonify({'error': f'Audio analysis failed: {str(e)}'}), 500

def extract_audio_features(audio_path):
    """Extract audio features from audio file"""
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Extract features
        # Pitch (fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr, threshold=0.1)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        pitch_mean = np.mean(pitch_values) if pitch_values else 150.0
        pitch_variance = np.var(pitch_values) if len(pitch_values) > 1 else 0.0
        
        # Speech rate estimation (very basic)
        # Count zero crossings as a proxy for speech activity
        zero_crossings = librosa.zero_crossings(y, pad=False)
        speech_rate = np.sum(zero_crossings) / len(y) * sr * 60 / 10  # Rough WPM estimate
        
        # Volume level (RMS energy)
        rms = librosa.feature.rms(y=y)[0]
        volume_level = np.mean(rms)
        
        # Voice tremor (pitch variance over time)
        voice_tremor = min(1.0, pitch_variance / 1000)  # Normalize
        
        # Pause frequency (silence detection)
        # Simple threshold-based silence detection
        frame_length = 2048
        hop_length = 512
        silence_threshold = 0.01
        
        frames = librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length)
        silence_frames = np.mean(np.abs(frames), axis=0) < silence_threshold
        pause_frequency = np.sum(silence_frames) / len(silence_frames)
        
        # Emotional tone estimation (very basic)
        # Based on spectral features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        
        if spectral_centroid > 3000 and pitch_variance > 500:
            emotional_tone = "distressed"
            tone_confidence = 0.7
        elif spectral_centroid > 2500:
            emotional_tone = "anxious"
            tone_confidence = 0.6
        elif spectral_centroid < 1500:
            emotional_tone = "depressed"
            tone_confidence = 0.6
        else:
            emotional_tone = "neutral"
            tone_confidence = 0.5
        
        return {
            'pitch_mean': float(pitch_mean),
            'pitch_variance': float(pitch_variance),
            'speech_rate': float(min(300, max(50, speech_rate))),  # Clamp to reasonable range
            'volume_level': float(min(1.0, volume_level * 10)),  # Normalize
            'voice_tremor': float(voice_tremor),
            'pause_frequency': float(pause_frequency),
            'emotional_tone': emotional_tone,
            'tone_confidence': float(tone_confidence)
        }
        
    except Exception as e:
        print(f"Audio feature extraction error: {str(e)}")
        # Return default features on error
        return {
            'pitch_mean': 180.0,
            'pitch_variance': 20.0,
            'speech_rate': 140.0,
            'volume_level': 0.5,
            'voice_tremor': 0.2,
            'pause_frequency': 0.3,
            'emotional_tone': 'neutral',
            'tone_confidence': 0.5
        }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'mental_health_sentiment_analyzer',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Mental Health Sentiment Analysis Test Server...")
    print("📊 Frontend available at: http://localhost:8080")
    print("🔗 API endpoints:")
    print("  • POST /analyze - Text analysis")
    print("  • POST /analyze_audio - Audio + text analysis")
    print("  • GET /health - Health check")
    print("\n🧠 Ready to analyze mental health conversations!")
    
    app.run(host='0.0.0.0', port=8080, debug=True)