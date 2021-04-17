"""empty message

Revision ID: 4ef10a151fc4
Revises: b8e4d2b80681
Create Date: 2021-02-11 18:46:24.131704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef10a151fc4'
down_revision = 'b8e4d2b80681'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_visible', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_visible')
    # ### end Alembic commands ###