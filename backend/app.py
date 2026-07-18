from flask import Flask, jsonify
from database import init_db

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Futsal Bracket API is running"
    })


@app.route("/init-db")
def initialize_database():
    try:
        init_db()
        return jsonify({
            "status": "success",
            "message": "Database initialized successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)