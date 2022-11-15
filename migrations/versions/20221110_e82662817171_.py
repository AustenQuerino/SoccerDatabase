"""empty message

Revision ID: e82662817171
Revises: 5627b8f6b3fe
Create Date: 2022-11-10 20:18:05.124235

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e82662817171'
down_revision = '5627b8f6b3fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leagues',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('commissioner', sa.String(length=128), nullable=True),
    sa.Column('calendar_year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=False),
    sa.Column('nation_abbreviation', sa.String(length=3), nullable=False),
    sa.Column('national_team', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['national_team'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('national_team')
    )
    op.create_table('stadiums',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stadium_name', sa.String(length=128), nullable=False),
    sa.Column('max_capacity', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=True),
    sa.Column('nation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nation'], ['nations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('team_name', sa.String(length=128), nullable=False),
    sa.Column('national_team', sa.Boolean(), nullable=False),
    sa.Column('manager_name', sa.String(length=128), nullable=True),
    sa.Column('home_stadium', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['home_stadium'], ['stadiums.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('team_name')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('committed_nation', sa.Integer(), nullable=True),
    sa.Column('club_team', sa.Integer(), nullable=True),
    sa.Column('national_team', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['club_team'], ['teams.id'], ),
    sa.ForeignKeyConstraint(['committed_nation'], ['nations.id'], ),
    sa.ForeignKeyConstraint(['national_team'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referees',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('leagues_registered', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['leagues_registered'], ['leagues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams_leagues',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('league_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['league_id'], ['leagues.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'league_id')
    )
    op.create_table('teams_stadiums',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('stadium_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['stadium_id'], ['stadiums.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'stadium_id')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('attendance', sa.Integer(), nullable=True),
    sa.Column('home_team', sa.Integer(), nullable=False),
    sa.Column('away_team', sa.Integer(), nullable=False),
    sa.Column('league', sa.Integer(), nullable=True),
    sa.Column('referee', sa.Integer(), nullable=False),
    sa.Column('stadium', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['away_team'], ['teams.id'], ),
    sa.ForeignKeyConstraint(['home_team'], ['teams.id'], ),
    sa.ForeignKeyConstraint(['league'], ['leagues.id'], ),
    sa.ForeignKeyConstraint(['referee'], ['referees.id'], ),
    sa.ForeignKeyConstraint(['stadium'], ['stadiums.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player_teams',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('player_id', 'team_id')
    )
    op.create_table('games.referee',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('referee_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['referee_id'], ['referees.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'referee_id')
    )
    op.create_table('games.stadiums',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('stadium_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['stadium_id'], ['stadiums.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'stadium_id')
    )
    op.create_table('teams.games',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'game_id')
    )
    op.drop_table('users')
    op.drop_table('likes')
    op.drop_table('tweets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tweets',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tweets_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(length=280), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='tweets_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tweets_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('likes',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('tweet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], name='likes_tweet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'tweet_id', name='likes_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    op.drop_table('teams.games')
    op.drop_table('games.stadiums')
    op.drop_table('games.referee')
    op.drop_table('player_teams')
    op.drop_table('games')
    op.drop_table('teams_stadiums')
    op.drop_table('teams_leagues')
    op.drop_table('referees')
    op.drop_table('players')
    op.drop_table('teams')
    op.drop_table('stadiums')
    op.drop_table('nations')
    op.drop_table('leagues')
    # ### end Alembic commands ###
