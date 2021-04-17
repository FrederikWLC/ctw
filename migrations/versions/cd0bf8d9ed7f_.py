"""empty message

Revision ID: cd0bf8d9ed7f
Revises: 61508164aaa1
Create Date: 2021-02-19 18:16:59.518884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd0bf8d9ed7f'
down_revision = '61508164aaa1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo', sa.Column('is_empty', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo', 'is_empty')
    # ### end Alembic commands ###