from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global call counter
call_counter = 1000

class CallData:
    def __init__(self, user_phone, user_name, call_duration, call_transcript, summary):
        self.id = 0
        self.user_phone = user_phone
        self.user_name = user_name
        self.call_duration = call_duration
        self.self_harm_percentage = -1
        self.homicidal_percentage = -1
        self.psychosis_percentage = -1
        self.distress_percentage = -1
        self.call_priority = "Analyzing"
        self.call_transcript = call_transcript
        self.summary = summary
    
    def update_status_percentages(self):
        if self.call_transcript is None:
            return

        # Make call to backend huggingface model
        url = "https://roshansanjeev-sentimentanalysis.hf.space/"
        payload = {"text": self.call_transcript}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            sentiment_analysis = response.json()
            print("Response:", sentiment_analysis)
        except requests.exceptions.RequestException as e:
            print(f"Error calling sentiment analysis API: {e}")
            return
        except json.JSONDecodeError:
            print(f"Error decoding JSON. Response: {response.text}")
            return

        def _normalize_score(score):
            """Normalize score to 0.99 if it's 1 or True, and 0.0 if None."""
            if score is True or score == 1:
                return 0.99
            if score is None:
                return 0.0
            return score

        self.self_harm_percentage = _normalize_score(sentiment_analysis.get("self_harm"))
        self.homicidal_percentage = _normalize_score(sentiment_analysis.get("homicidal"))
        self.psychosis_percentage = _normalize_score(sentiment_analysis.get("psychosis"))
        self.distress_percentage = _normalize_score(sentiment_analysis.get("distress"))

        return sentiment_analysis
    
    def update_call_priority(self):
        # The line below will cause a TypeError because call_duration is a string.
        # This logic is commented out for now.
        # if self.call_duration < 10:
        #     self.call_priority = "Analyzing"
        #     return self.call_priority

        if (self.homicidal_percentage is not None and self.homicidal_percentage > 80.0) or \
           (self.psychosis_percentage is not None and self.psychosis_percentage > 80.0) or \
           (self.distress_percentage is not None and self.distress_percentage > 80.0):
            self.call_priority = "High Priority"
        else:
            self.call_priority = "Normal" 
        
        return self.call_priority


@app.route('/vapi-webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    global call_counter

    # If there are no calls going on
    if data == None:
        return '', 204
    
    # If there are calls going on return data in the following format
    else:
        ####################################################################################################
        #######################Code to extract variables goes here######################### ############## 
        ####### Edit the data varaible to turn into a list to populate the CallData class below ############## 
        ####################################################################################################

        # Handle both single object and list of objects
        if isinstance(data, list):
            # If data is a list, take the first item
            call_data = data[0] if data else {}
        else:
            # If data is a single object
            call_data = data

        call_counter += 1
        new_call = CallData(
            user_phone=call_data.get("user_phone"),
            user_name=call_data.get("user_name"),
            call_duration=call_data.get("call_duration"),
            call_transcript=call_data.get("call_transcript"),
            summary=call_data.get("summary")
        )
        new_call.id = call_counter
        new_call.update_status_percentages()
        new_call.update_call_priority()
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        print("Priority: ", new_call.call_priority)

        # Broadcast to frontend via WebSocket
        print(f"📡 Broadcasting call to WebSocket: {new_call.__dict__}")
        socketio.emit('new_call', new_call.__dict__)
        print("✅ WebSocket emission completed")

        return jsonify(new_call.__dict__), 200


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)