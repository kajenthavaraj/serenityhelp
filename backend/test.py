from flask import Flask, request
import json
import time

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
            # Initialize session if new
            if call_id not in live_sessions:
                live_sessions[call_id] = {
                    "phone": user_phone,
                    "user_name": "Unknown",
                    "messages": [],
                    "start_time": time.time()
                }

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

                live_sessions[call_id]["messages"].append({
                    "role": role,
                    "message": content,
                    "time": timestamp
                })

                # 🧠 Name extraction from user input
                if role == "user":
                    content_lower = content.lower()
                    non_name_words = {"not", "okay", "fine", "unsure", "tired", "good", "alright", "sure", "here"}

                    if "my name is" in content_lower:
                        parts = content.split("my name is", 1)[1].strip().split()
                        if parts:
                            name = parts[0].capitalize()
                            live_sessions[call_id]["user_name"] = name
                            print(f"👤 Captured user name: {name}")

                    elif (content_lower.startswith("i'm ") or content_lower.startswith("i am ")) and len(content.split()) == 2:
                        possible_name = content.split(" ", 1)[1].strip().split()[0].capitalize()
                        if possible_name.lower() not in non_name_words:
                            live_sessions[call_id]["user_name"] = possible_name
                            print(f"👤 Captured user name: {possible_name}")

                # 🤖 Name extraction from bot reply
                if role == "bot" and live_sessions[call_id]["user_name"] == "Unknown":
                    content_lower = content.lower()
                    for phrase in ["nice to meet you,", "thank you for sharing that,", "it's good to meet you,", "it's okay to take your time,"]:
                        if phrase in content_lower:
                            try:
                                name = content.split(phrase, 1)[1].strip().split()[0].capitalize()
                                live_sessions[call_id]["user_name"] = name
                                print(f"🤖 Captured user name from assistant reply: {name}")
                            except IndexError:
                                pass

    elif msg_type == "end-of-call-report":
        session = live_sessions.get(call_id)
        if session:
            print(f"\n📞 Final transcript for {session.get('user_name', 'Unknown')} ({session['phone']}):")
            for m in session["messages"]:
                print(f"{m['role'].capitalize()}: {m['message']}")

            duration = time.time() - session["start_time"]
            print(f"\n⏱️ Total call duration: {duration:.1f} seconds")

            del live_sessions[call_id]

        summary = message.get("analysis", {}).get("summary", "")
        print("\n🧠 Summary:")
        print(summary)

    return '', 200

if __name__ == '__main__':
    app.run(port=5001)
