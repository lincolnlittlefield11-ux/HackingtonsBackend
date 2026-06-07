from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
import os

app = Flask(__name__)

CORS(app, origins=["https://www.hackingtons.io"])

client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing message"}), 400

        user_message = data["message"]

        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = response.content[0].text

        return jsonify({
            "response": reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
