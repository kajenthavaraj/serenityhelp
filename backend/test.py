from flask import Flask, request
import json
import time
import re
import requests

app = Flask(__name__)

# Global in-memory dictionary to store session data per call_id
live_sessions = {}

@app.route('/vapi-webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    message = data.get("message", {})
    msg_type = message.get("type")
    call_info = message.get("call", {})
    call_id = call_info.get("id")

    if msg_type == "speech-update":
        artifact = message.get("artifact", {})
        messages = artifact.get("messages", [])
        user_phone = message.get("customer", {}).get("number", "Unknown")

        if call_id:
            is_new_session = False

            # Initialize session if new
            if call_id not in live_sessions:
                live_sessions[call_id] = {
                    "phone": user_phone,
                    "user_name": "Unknown",
                    "messages": [],
                    "start_time": time.time()
                }
                is_new_session = True

            # ✅ On first speech-update, trigger a new_call to dashboard
            if is_new_session:
                init_data = {
                    "id": int(time.time()),  # fallback ID
                    "user_phone": user_phone,
                    "user_name": "Unknown",
                    "call_duration": "0.0",
                    "call_transcript": "",
                    "summary": "Call in progress..."
                }
                try:
                    requests.post("http://localhost:5001/vapi-webhook", json=init_data)
                    print("📤 Initial new_call sent to output server")
                except Exception as e:
                    print(f"❌ Failed to send initial new_call: {e}")

            # Show elapsed call time
            elapsed = time.time() - live_sessions[call_id]["start_time"]
            print(f"📞 Live message from: {user_phone} | ⏱️ Elapsed time: {elapsed:.1f} seconds")

            for m in messages:
                role = m.get("role")
                if role == "system":
                    continue

                content = m.get("message")
                timestamp = m.get("time")

                print(f"{role.capitalize()}: {content} (at {timestamp})")

                msg_obj = {
                    "role": role,
                    "message": content,
                    "time": timestamp
                }

                prev_messages = live_sessions[call_id]["messages"]
                recent_messages = prev_messages[-3:] if len(prev_messages) >= 3 else prev_messages

                is_duplicate = any(
                    msg["message"] == content and msg["role"] == role
                    for msg in recent_messages
                )

                if not is_duplicate:
                    live_sessions[call_id]["messages"].append(msg_obj)

                    if len(prev_messages) == 0:
                        new_call_data = {
                            "id": int(time.time()),
                            "user_phone": user_phone,
                            "user_name": live_sessions[call_id]["user_name"],
                            "call_duration": "0.0",
                            "call_transcript": "",
                            "summary": "Call in progress..."
                        }
                        try:
                            requests.post("http://localhost:5001/vapi-webhook", json=new_call_data)
                            print("📤 New call POSTED to dashboard (from test.py)")
                        except Exception as e:
                            print(f"❌ Failed to POST new call: {e}")

                    # 🧠 Name extraction from user input
                    if role == "user" and live_sessions[call_id]["user_name"] == "Unknown":
                        match = re.search(r"\b(my name is|i am|i'm)\s+([A-Z][a-z]+)", content, re.IGNORECASE)
                        if match:
                            name = match.group(2).capitalize()
                            live_sessions[call_id]["user_name"] = name
                            print(f"👤 Captured user name: {name}")

                    # 🤖 Name extraction from bot
                    if role == "bot" and live_sessions[call_id]["user_name"] == "Unknown":
                        match = re.search(
                            r"(?:nice to meet you|thank you for sharing that|it's good to meet you|it's okay to take your time),?\s+([A-Z][a-z]+)",
                            content,
                            re.IGNORECASE
                        )
                        if match:
                            name = match.group(1).capitalize()
                            live_sessions[call_id]["user_name"] = name
                            print(f"🤖 Captured user name from assistant reply: {name}")

                    live_data = {
                        "call_id": call_id,
                        "user_phone": user_phone,
                        "user_name": live_sessions[call_id]["user_name"],
                        "role": role,
                        "message": content,
                        "timestamp": timestamp
                    }

                    try:
                        requests.post("http://localhost:5001/live-update", json=live_data)
                        print(f"📤 Live update sent: {live_data}")
                    except Exception as e:
                        print(f"❌ Failed to send live update: {e}")
                else:
                    print(f"⚠️ Duplicate skipped: {role}: {content}")

    elif msg_type == "end-of-call-report":
        session = live_sessions.get(call_id)
        if session:
            print(f"\n📞 Final transcript for {session.get('user_name', 'Unknown')} ({session['phone']}):")
            transcript_lines = []
            for m in session["messages"]:
                line = f"{m['role'].capitalize()}: {m['message']}"
                transcript_lines.append(line)
                print(line)

            duration = time.time() - session["start_time"]
            print(f"\n⏱️ Total call duration: {duration:.1f} seconds")

            summary = message.get("analysis", {}).get("summary", "")
            print("\n🧠 Summary:")
            print(summary)

            call_data = {
                "user_phone": session["phone"],
                "user_name": session["user_name"],
                "call_duration": f"{duration:.1f}",
                "call_transcript": "\n".join(transcript_lines),
                "summary": summary
            }

            try:
                print("📤 Sending final call data to output server...")
                response = requests.post("http://localhost:5001/vapi-webhook", json=call_data)
                print(f"✅ Response from output server: {response.status_code} {response.text}")
            except Exception as e:
                print(f"❌ Failed to send final call data: {e}")

            del live_sessions[call_id]

    return '', 200

if __name__ == '__main__':
    app.run(port=5002)
