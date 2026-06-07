from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Allow Hackingtons
CORS(app, origins=["https://www.hackingtons.io"])

HF_TOKEN = os.environ["HF_API_KEY"]

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/test")
def test():
    try:
        r = requests.get("https://huggingface.co", timeout=10)
        return f"Hugging Face reachable. Status: {r.status_code}"
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing message"}), 400

        user_message = data["message"]

        payload = {
            "inputs": user_message,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7
            }
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        if isinstance(result, list):
            reply = result[0].get("generated_text", "No text returned")
        else:
            reply = str(result)

        return jsonify({
            "response": reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
