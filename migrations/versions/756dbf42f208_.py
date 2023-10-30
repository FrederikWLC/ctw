"""empty message

Revision ID: 756dbf42f208
Revises: ebf3439e2589
Create Date: 2023-09-07 23:46:38.515398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '756dbf42f208'
down_revision = 'ebf3439e2589'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('erc360', schema=None) as batch_op:
        batch_op.add_column(sa.Column('symbol', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('erc360', schema=None) as batch_op:
        batch_op.drop_column('symbol')

    # ### end Alembic commands ###