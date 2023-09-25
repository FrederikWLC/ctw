"""empty message

Revision ID: eb9c45a803b4
Revises: 3cee14c42129
Create Date: 2023-09-25 14:52:26.660620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb9c45a803b4'
down_revision = '3cee14c42129'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('erc360_token_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token_id', sa.BigInteger(), nullable=True))
        batch_op.drop_column('creation_clock')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('erc360_token_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_clock', sa.BIGINT(), autoincrement=False, nullable=True))
        batch_op.drop_column('token_id')

    # ### end Alembic commands ###
