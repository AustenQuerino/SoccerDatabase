from flask import Blueprint, jsonify, abort, request 
from ..models import Player, Team, League, Nation, Stadium, Game, Referee, db 

bp = Blueprint('players', __name__, url_prefix='/players')
# Decorator takes path and list of HTTP verbs
@bp.route('', methods=['GET'])
def index():
    # ORM performs SELECT query
    players = Player.query.all()
    result = []
    for p in players:
        # build list of Players as dictionaries
        result.append(p.serialize())
    # return JSON response
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Player.query.get_or_404(id)
    return jsonify(p.serialize())

@bp.route('', methods=['POST'])
def create():
    # Req body must contain club_team
    if 'club_team' not in request.json:
        return abort(400)
    # Team with id of team_id must exist 
    Team.query.get_or_404(request.json['club_team'])
    # Construct Player
    p = Player(
        birth_year=request.json['birth_year'],
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        committed_nation=request.json['committed_nation'],
        club_team=request.json['club_team'],
        national_team=request.json['national_team']
    )
    # Prepare CREATE statement 
    db.session.add(p)
    # Eecture CREATE statement 
    db.session.commit()
    return jsonify(p.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Player.query.get_or_404(id)
    try:
        # Prepare DELETE statement
        db.session.delete(p)
        # Execute DELETE statement 
        db.session.commit()
        return jsonify(True)
    except:
        # Something went wrong
        return jsonify(False)

@bp.route('/<int:id>/player_teams', methods=['GET'])
def player_team(id: int):
    t = Team.query.get_or_404(id)
    result = []
    for t in t.player_team:
        result.append(t.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    p = Player.query.get_or_404(id)
    if 'first_name' not in request.json or 'last_name' not in request.json:
        return abort(400)
    p.birth_year=request.json['birth_year']
    p.first_name=request.json['first_name']
    p.last_name=request.json['last_name']
    p.committed_nation=request.json['committed_nation']
    p.club_team=request.json['club_team']
    p.national_team=request.json['national_team']
    try:
        db.session.commit()
        return jsonify(p.serialize())
    except:
        # Something was missing
        return jsonify(False)
