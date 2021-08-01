"""empty message

Revision ID: cd4bbef5f612
Revises: 1376f17e9d53
Create Date: 2021-08-01 18:41:53.297304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd4bbef5f612'
down_revision = '1376f17e9d53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('creation_datetime', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('to_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['to_id'], ['feedback.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feedback_creation_datetime'), 'feedback', ['creation_datetime'], unique=False)
    op.add_column('post', sa.Column('public', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'public')
    op.drop_index(op.f('ix_feedback_creation_datetime'), table_name='feedback')
    op.drop_table('feedback')
    # ### end Alembic commands ###
