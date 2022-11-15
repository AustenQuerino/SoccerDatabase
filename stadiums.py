from flask import Blueprint, jsonify, abort, request 
from ..models import Player, Team, League, Nation, Stadium, Game, Referee, db 

bp = Blueprint('stadiums', __name__, url_prefix='/stadiums')

@bp.route('', methods=['GET'])
def index():
    stadiums = Stadium.query.all()
    result = []
    for s in stadiums:
        result.append(s.serialize())
    return jsonify(result)

@bp.route('', methods=['POST'])
def create():
    if 'nation' not in request.json:
        return abort(400)
    # Construct Stadium
    s = Stadium(
        stadium_name=request.json['stadium_name'],
        max_capacity=request.json['max_capacity'], 
        city=request.json['city'],
        nation=request.json['nation']
    )
    # Prepare CREATE statement
    db.session.add(s)
    # Execute CREATE statement 
    db.session.commit()
    return jsonify(s.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    s = Stadium.query.get_or_404(id)
    try:
        # Prepare DELETE statement
        db.session.delete(s)
        # Execute DELETE statement 
        db.session.commit()
        return jsonify(True)
    except:
        # Something went wrong
        return jsonify(False)