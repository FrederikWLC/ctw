"""empty message

Revision ID: 7711ae477bff
Revises: bd58b3d44078
Create Date: 2021-06-25 22:19:18.484089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7711ae477bff'
down_revision = 'bd58b3d44078'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club_viewers',
    sa.Column('club_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('project_viewers',
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_viewers')
    op.drop_table('club_viewers')
    # ### end Alembic commands ###
