from flask import Blueprint, jsonify, abort, request 
from ..models import Player, Team, League, Nation, Stadium, Game, Referee, db

bp = Blueprint('games', __name__, url_prefix='/games')

# Decorator takes path and list of HTTP verbs 
@bp.route('', methods=['GET'])
def index():
    # ORM performs SELECT query 
    games = Game.query.all()
    result = []
    for g in games:
        result.append(g.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    g = Game.query.get_or_404(id)
    return jsonify(g.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'league_id' not in request.json or 'home_team' not in request.json or 'away_team' not in request.json:
        return abort(400)
    # Construct Game
    g = Game(
        date=request.json['date'],
        attendance=request.json['attendance'],
        home_team=request.json['home_team'], 
        away_team=request.json['away_team'],
        league_id=request.json['league_id'],
        referee=request.json['referee'],
        stadium=request.json['stadium']
    )
    # Prepare CREATE statement
    db.session.add(g)
    # Execute CREATE statement 
    db.session.commit()
    return jsonify(g.serialize())


@bp.route('/<int:int>', methods=['DELETE'])
def delete(id: int):
    g = Game.query.get_or_404(id)
    try:
        db.session.delete(g)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

