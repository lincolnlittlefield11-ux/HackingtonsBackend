from flask import Flask, request, jsonify
from flask_cors import CORS
from anthropic import Anthropic
import os

app = Flask(__name__)

# Allow requests from Hackingtons
CORS(app, origins=["https://www.hackingtons.io"])

# Claude client (uses Render environment variable)
client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

@app.route("/", methods=["GET"])
def home():
    return "Backend is running!"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # Handle CORS preflight request
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.get_json()
        user_message = data["message"]

        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=500,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({
            "response": response.content[0].text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)