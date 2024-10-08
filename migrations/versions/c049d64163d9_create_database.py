"""Create database

Revision ID: c049d64163d9
Revises: 
Create Date: 2023-06-07 16:09:24.089013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c049d64163d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zodiac_signs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('horoscope_data',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('zodiac_sign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['zodiac_sign_id'], ['zodiac_signs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('horoscope_data')
    op.drop_table('zodiac_signs')
    # ### end Alembic commands ###
