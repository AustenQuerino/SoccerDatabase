from flask import Blueprint, jsonify, abort, request
from ..models import Player, Team, League, Nation, Stadium, Game, Referee, db

bp = Blueprint('teams', __name__, url_prefix='/teams')
# Decorator takes path and list of HTTP verbs
@bp.route('', methods=['GET'])
def index():
    # ORM performs SELECT query 
    teams = Team.query.all()
    result = []
    for t in teams:
        # build list of Teams as dictionaries
        result.append(t.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Team.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('',methods=['POST'])
def create():
    # Req body must contain league
    if 'league_id' not in request.json or 'team_name' not in request.json:
        return abort(400)
    # League wit id of league_is must exist 
    League.query.get_or_404(request.json['league_id'])
    # Construct Team
    t = Team(
        league_id=request.json['league_id'],
        team_name=request.json['team_name'],
        national_team=request.json['national_team'],
        manager_name=request.json['manager_name'],
        home_stadium=request.json['home_stadium']
    )
    # Prepare CREATE statement 
    db.session.add(t)
    # Eecture CREATE statement 
    db.session.commit()
    return jsonify(t.serialize())



@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Team.query.get_or_404(id)
    try:
        db.session.delete(t)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

@bp.route('/<int:id>/player_teams', methods=['GET'])
def player_teams(id: int):
    p = Player.query.get_or_404(id)
    result = []
    for p in p.player_teams:
        result.append(p.serialize())
    return jsonify(result)

