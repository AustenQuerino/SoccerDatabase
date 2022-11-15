from flask import Blueprint, jsonify, abort, request 
from ..models import Player, Team, League, Nation, Stadium, Game, Referee, db

bp = Blueprint('leagues', __name__, url_prefix='/leagues')

# Decorator takes path and list of HTTP verbs 
@bp.route('', methods=['GET'])
def index():
    # ORM performs SELECT query 
    league = League.query.all()
    result = []
    for l in league:
        result.append(l.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = League.query.get_or_404(id)
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    # Req body must contain calendar_year
    if 'calendar_year' not in request.json or 'league_name' not in request.json:
        return abort(400)
    # Construct League
    l = League(
        league_name=request.json['league_name'],
        commissioner=request.json['commissioner'],
        calendar_year=request.json['calendar_year']
    )
    # Prepare CREATE statement
    db.session.add(l)
    # Execute CREATE statement 
    db.session.commit()
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    l = League.query.get_or_404(id)
    try:
        db.session.delete(l)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
