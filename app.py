from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

CORS(app, origins=["https://www.hackingtons.io"])

HF_TOKEN = os.environ["HF_API_KEY"]

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route("/", methods=["GET"])
def home():
    return "Backend is running!"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.get_json()
        user_message = data["message"]

        payload = {
            "inputs": user_message,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        result = response.json()

        # Hugging Face returns different formats sometimes
        if isinstance(result, list):
            reply = result[0]["generated_text"]
        else:
            reply = result.get("error", "No response")

        return jsonify({
            "response": reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)