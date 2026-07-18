from flask import Flask, jsonify, request, render_template
from database import init_db, SessionLocal
from models import Team, Match

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api_home():
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


@app.route("/matches", methods=["GET"])
def get_matches():
    db = SessionLocal()
    try:
        matches = db.query(Match).order_by(Match.id.asc()).all()

        result = []
        for match in matches:
            result.append({
                "id": match.id,
                "round_name": match.round_name,
                "match_code": match.match_code,
                "team1_id": match.team1_id,
                "team2_id": match.team2_id,
                "team1_name": match.team1.name if match.team1 else None,
                "team2_name": match.team2.name if match.team2 else None,
                "home_score": match.home_score,
                "away_score": match.away_score,
                "winner_id": match.winner_id,
                "winner_name": match.winner.name if match.winner else None
            })

        return jsonify(result)
    finally:
        db.close()


@app.route("/matches", methods=["POST"])
def create_match():
    db = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body harus JSON"
            }), 400

        round_name = data.get("round_name")
        match_code = data.get("match_code")
        team1_id = data.get("team1_id")
        team2_id = data.get("team2_id")

        if not round_name or not match_code or not team1_id or not team2_id:
            return jsonify({
                "status": "error",
                "message": "round_name, match_code, team1_id, dan team2_id wajib diisi"
            }), 400

        if team1_id == team2_id:
            return jsonify({
                "status": "error",
                "message": "Team 1 dan Team 2 tidak boleh sama"
            }), 400

        team1 = db.query(Team).filter(Team.id == team1_id).first()
        team2 = db.query(Team).filter(Team.id == team2_id).first()

        if not team1 or not team2:
            return jsonify({
                "status": "error",
                "message": "Salah satu team tidak ditemukan"
            }), 400

        existing_match = db.query(Match).filter(Match.match_code == match_code).first()
        if existing_match:
            return jsonify({
                "status": "error",
                "message": "Match code sudah digunakan"
            }), 400

        new_match = Match(
            round_name=round_name,
            match_code=match_code,
            team1_id=team1_id,
            team2_id=team2_id
        )

        db.add(new_match)
        db.commit()
        db.refresh(new_match)

        return jsonify({
            "status": "success",
            "message": "Match berhasil ditambahkan",
            "data": {
                "id": new_match.id,
                "round_name": new_match.round_name,
                "match_code": new_match.match_code,
                "team1_id": new_match.team1_id,
                "team2_id": new_match.team2_id
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


@app.route("/matches/<int:match_id>/score", methods=["PUT"])
def update_match_score(match_id):
    db = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body harus JSON"
            }), 400

        home_score = data.get("home_score")
        away_score = data.get("away_score")

        if home_score is None or away_score is None:
            return jsonify({
                "status": "error",
                "message": "home_score dan away_score wajib diisi"
            }), 400

        try:
            home_score = int(home_score)
            away_score = int(away_score)
        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": "Skor harus berupa angka"
            }), 400

        if home_score < 0 or away_score < 0:
            return jsonify({
                "status": "error",
                "message": "Skor tidak boleh negatif"
            }), 400

        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            return jsonify({
                "status": "error",
                "message": "Match tidak ditemukan"
            }), 404

        match.home_score = home_score
        match.away_score = away_score

        if home_score > away_score:
            match.winner_id = match.team1_id
        elif away_score > home_score:
            match.winner_id = match.team2_id
        else:
            match.winner_id = None

        db.commit()
        db.refresh(match)

        return jsonify({
            "status": "success",
            "message": "Skor match berhasil diupdate",
            "data": {
                "id": match.id,
                "match_code": match.match_code,
                "home_score": match.home_score,
                "away_score": match.away_score,
                "winner_id": match.winner_id,
                "winner_name": match.winner.name if match.winner else None
            }
        })
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