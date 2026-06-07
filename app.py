from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

CORS(app, origins=["https://www.hackingtons.io"])

# OpenAI client
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

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

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({
            "response": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)