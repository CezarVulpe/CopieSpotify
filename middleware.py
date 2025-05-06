from flask import Flask, request, jsonify
from flask_cors import CORS
import socket

app = Flask(__name__)

SERVER_HOST = "192.168.18.138"  # IP-ul mașinii cu `main.py`
SERVER_PORT = 12345
CORS(app)

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"status": "error", "message": "Missing username"}), 400

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.send(f"add_user:{username}".encode())
            response = s.recv(1024).decode()
        return jsonify({"status": "success", "message": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
