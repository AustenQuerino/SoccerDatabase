"""empty message

Revision ID: df4817b80902
Revises: 9e3642368ea3
Create Date: 2022-11-11 16:09:29.343863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df4817b80902'
down_revision = '9e3642368ea3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'leagues', ['league_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'leagues', type_='unique')
    # ### end Alembic commands ###
