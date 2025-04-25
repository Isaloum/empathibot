import firebase_admin
from firebase_admin import credentials, firestore


from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os

load_dotenv()
import json
firebase_json = os.getenv("FIREBASE_CONFIG_JSON")
cred = credentials.Certificate(json.loads(firebase_json))

firebase_admin.initialize_app(cred)
db = firestore.client()

llm = OpenAI(temperature=0.7)

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        incoming_msg = request.form.get("Body", "").strip()
        sender = request.form.get("From", "")  # 🆕 Who sent the message?

        response = llm.invoke(f"Respond empathetically to this message: {incoming_msg}")

        # 🆕 Save full context to Firestore
        db.collection("messages").add({
            "text": incoming_msg,
            "response": str(response),  # ✅ Save bot’s reply too
            "sender": sender,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        print(f"User ({sender}): {incoming_msg}")
        print(f"Empathibot: {response}")

        twilio_response = MessagingResponse()
        twilio_response.message(str(response))
        return str(twilio_response)

    except Exception as e:
        # 🛑 Log errors in Firestore
        db.collection("errors").add({
            "error": str(e),
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"[ERROR] {e}")
        return "Internal server error", 500
    @app.route("/health", methods=["GET"])
def health():
    return "Empathibot is alive!", 200
    
    if __name__ == "__main__":
         print("✅ Flask app is starting properly on Render...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



