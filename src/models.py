from flask_sqlalchemy import SQLAlchemy
import datetime

'''Create a Database Adapter Object'''
db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String, unique=True, nullable=False)
    national_team = db.Column(db.Boolean, nullable=False)
    manager_name = db.Column(db.String)
    home_stadium = db.Column(db.Integer, db.ForeignKey('stadiums.id'), nullable=False)

    def __init__(self, team_name: str, national_team: bool, manager_name: str, 
                    home_stadium: int):
        self.team_name = team_name
        self.national_team = national_team
        self.manager_name = manager_name
        self.home_stadium = home_stadium

    def serialize(self):
        return {
            'id': self.id,
            'team_name': self.team_name, 
            'national_team': self.national_team,
            'manager_name': self.manager_name,
            'home_stadium': self.home_stadium
        }

player_teams = db.Table(
    'player_teams',
    db.Column(
        'player_id', db.Integer,
        db.ForeignKey('players.id'),
        primary_key=True
    ),
    db.Column(
        'team_id', db.Integer,
        db.ForeignKey('teams.id'),
        primary_key=True
    ),
    # db.Column(
    #     'created_at', db.DateTime,
    #     default=datetime.datetime.utcnow,
    #     nullable=False
    # )
)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birth_year = db.Column(db.Integer)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    committed_nation = db.Column(db.Integer, db.ForeignKey('nations.id'), nullable=False)
    club_team = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    national_team = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    # References to another table
    # teams = db.relationship('Team', backref='player', cascade='all,delete')

    player_team = db.relationship(
        'Team', secondary=player_teams, 
        lazy='subquery',
        backref=db.backref('teams_players', lazy=True)
    )

    def __init__(self, birth_year: int, first_name: str, last_name: str, 
                    committed_nation: int, club_team: int, national_team: int):
        self.birth_year = birth_year
        self.first_name = first_name
        self.last_name = last_name
        self.committed_nation = committed_nation
        self.club_team = club_team
        self.national_team = national_team

    def serialize(self):
        return {
            'id': self.id,
            'birth_year': self.birth_year,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'committed_nation': self.committed_nation,
            'club_team': self.club_team,
            'national_team': self.national_team
        }

class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league_name = db.Column(db.String, unique=True)
    commissioner = db.Column(db.String)
    calendar_year = db.Column(db.Integer, nullable=False)

    def __init__(self, league_name: str, commissioner: str, 
                    calendar_year: int):
        self.league_name = league_name
        self.commissioner = commissioner
        self.calendar_year = calendar_year

    def serialize(self):
        return {
            'id': self.id,
            'league_name': self.league_name,
            'commissioner': self.commissioner,
            'calendar_year': self.calendar_year
        }

class Nation(db.Model):
    __tablename__ = 'nations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    nation_abbreviation = db.Column(db.String(3), nullable=False)
    national_team = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=True)

class Stadium(db.Model):
    __tablename__ = 'stadiums'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stadium_name = db.Column(db.String, nullable=False)
    max_capacity = db.Column(db.Integer)
    city = db.Column(db.String)
    nation = db.Column(db.Integer, db.ForeignKey('nations.id'))

    def __init__(self, stadium_name: str, max_capacity: int, city: str, nation: int):
        self.stadium_name = stadium_name
        self.max_capacity = max_capacity
        self.city = city
        self.nation = nation
    
    def serialize(self):
        return {
            'id': self.id,
            'stadium_name': self.stadium_name,
            'max_capacity': self.max_capacity, 
            'city': self.city,
            'nation': self.nation 
        }

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    attendance = db.Column(db.Integer)
    home_team = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    league = db.Column(db.Integer, db.ForeignKey('leagues.id'))
    referee = db.Column(db.Integer, db.ForeignKey('referees.id'), nullable=False)
    stadium = db.Column(db.Integer, db.ForeignKey('stadiums.id'))

    def __init__(self, date: date, attendance: int, home_team: int, 
                    away_team: int, league_id: int, referee: int, stadium: int):
        self.date = date
        self.attendance = attendance
        self.home_team = home_team
        self.away_team = away_team
        self.league_id = league_id
        self.referee = referee
        self.stadium = stadium

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'attendance': self.attendance,
            'home_team': self.home_team,
            'away_team': self.away_team, 
            'league': self.league,
            'referee': self.referee,
            'stadium': self.stadium
        }

class Referee(db.Model):
    __tablename__ = 'referees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    leagues_registered = db.Column(db.Integer, db.ForeignKey('leagues.id'))

    def __init__(self, name: str, leagues_registered: int): 
        self.name = name
        self.leagues_registered = leagues_registered
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'leagues_registered': self.leagues_registered
        }

'''Bridge Tables'''

teams_stadiums = db.Table(
    'teams_stadiums',
    db.Column(
        'team_id', db.Integer, 
        db.ForeignKey('teams.id'),
        primary_key=True
    ),
    db.Column(
        'stadium_id', db.Integer, 
        db.ForeignKey('stadiums.id'),
        primary_key=True
    )
)

teams_leagues = db.Table(
    'teams_leagues',
    db.Column(
        'team_id', db.Integer,
        db.ForeignKey('teams.id'),
        primary_key=True
    ),
    db.Column(
        'league_id', db.Integer, 
        db.ForeignKey('leagues.id'),
        primary_key=True
    )
)

teams_games = db.Table(
    'teams.games',
    db.Column(
        'team_id', db.Integer,
        db.ForeignKey('teams.id'),
        primary_key=True
    ),
    db.Column(
        'game_id', db.Integer, 
        db.ForeignKey('games.id'),
        primary_key=True
    )
)

games_referee = db.Table(
    'games.referee',
    db.Column(
        'game_id', db.Integer,
        db.ForeignKey('games.id'),
        primary_key=True
    ),
    db.Column(
        'referee_id', db.Integer,
        db.ForeignKey('referees.id'),
        primary_key=True
    )
)

games_stadiums = db.Table(
    'games.stadiums',
    db.Column(
        'game_id', db.Integer,
        db.ForeignKey('games.id'),
        primary_key=True
    ),
    db.Column(
        'stadium_id', db.Integer,
        db.ForeignKey('stadiums.id'),
        primary_key=True
    )
)

