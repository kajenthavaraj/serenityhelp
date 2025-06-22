from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

class CallData:
    def __init__(self, user_phone, user_name, call_duration, call_transcript, summary):
        self.user_phone = user_phone
        self.user_name = user_name
        self.call_duration = call_duration
        self.self_harm_percentage = -1
        self.homicidal_percentage = -1
        self.psychosis_percentage = -1
        self.distress_percentage = -1
        self.call_priority = -1
        self.call_transcript = call_transcript
        self.summary = summary
    
    def update_status_percentages(self):
        if self.call_transcript == None:
            return

        # Make call to backend huggingface model
        url = "https://roshansanjeev-sentimentanalysis.hf.space/"
        payload = {
            "text": self.call_transcript
        }

        response = requests.post(url, json=payload)
        print("Response:", response.json()) 

        # Get the sentiment analysis from the response
        sentiment_analysis = response.json()
        self.self_harm_percentage = sentiment_analysis.get("self_harm")
        self.homicidal_percentage = sentiment_analysis.get("homicidal")
        self.psychosis_percentage = sentiment_analysis.get("psychosis")
        self.distress_percentage = sentiment_analysis.get("distress")

        return response.json()


@app.route('/vapi-webhook', methods=['POST'])
def handle_webhook():
    data = request.json

    # If there are no calls going on
    if data == None:
        return '', 204
    
    # If there are calls going on return data in the following format
    else:
        ####################################################################################################
        #######################Code to extract variables goes here######################### ############## 
        ####### Edit the data varaible to turn into a list to populate the CallData class below ############## 
        ####################################################################################################

        list_of_calls = []
        for call in data:
            call_data = CallData(
                user_phone=call.get("user_phone"),
                user_name=call.get("user_name"),
                call_duration=call.get("call_duration"),
                call_transcript=call.get("call_transcript"),
                summary=call.get("summary")
            )
            call_data.update_status_percentages()
            list_of_calls.append(call_data)

        return jsonify(list_of_calls), 200

if __name__ == '__main__':
    app.run(port=5000)
