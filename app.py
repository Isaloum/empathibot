from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os

load_dotenv()
llm = OpenAI(temperature=0.7)

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "").strip()
    print(f"User: {incoming_msg}")

    response = llm.invoke(f"Respond empathetically to this message: {incoming_msg}")
    print(f"Empathibot: {response}")

    twilio_response = MessagingResponse()
    twilio_response.message(str(response))
    return str(twilio_response)

# ✅ Render-compatible server config
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s assigned port
    app.run(host="0.0.0.0", port=port)        # Listen on all interfaces
