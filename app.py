from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "¡Hola, mundo!"

@app.route("/webhook", methods=["POST"])
def webhook():
    # Procesar la solicitud de Telegram
    data = request.get_json()
    # ...
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)