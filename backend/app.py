from flask import Flask, jsonify, request
from database import init_db, SessionLocal
from models import Team

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


@app.route("/teams", methods=["GET"])
def get_teams():
    db = SessionLocal()
    try:
        teams = db.query(Team).order_by(Team.id.asc()).all()
        return jsonify([
            {
                "id": team.id,
                "name": team.name,
                "category": team.category
            }
            for team in teams
        ])
    finally:
        db.close()


@app.route("/teams", methods=["POST"])
def create_team():
    db = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body harus JSON"
            }), 400

        name = data.get("name")
        category = data.get("category")

        if not name or not category:
            return jsonify({
                "status": "error",
                "message": "name dan category wajib diisi"
            }), 400

        existing_team = db.query(Team).filter(Team.name == name).first()
        if existing_team:
            return jsonify({
                "status": "error",
                "message": "Team dengan nama itu sudah ada"
            }), 400

        new_team = Team(name=name, category=category)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)

        return jsonify({
            "status": "success",
            "message": "Team berhasil ditambahkan",
            "data": {
                "id": new_team.id,
                "name": new_team.name,
                "category": new_team.category
            }
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)