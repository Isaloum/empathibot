import firebase_admin
from firebase_admin import credentials, firestore


from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os

load_dotenv()
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

llm = OpenAI(temperature=0.7)

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "").strip()
    db.collection("messages").add({
    "text": incoming_msg,
    "timestamp": firestore.SERVER_TIMESTAMP
})

    print(f"User: {incoming_msg}")

    response = llm.invoke(f"Respond empathetically to this message: {incoming_msg}")
    print(f"Empathibot: {response}")

    twilio_response = MessagingResponse()
    twilio_response.message(str(response))
    return str(twilio_response)

# ✅ Render-compatible startup block
if __name__ == "__main__":
    print("✅ Flask app is starting properly on Render...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
