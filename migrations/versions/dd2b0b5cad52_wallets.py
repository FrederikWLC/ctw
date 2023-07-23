"""wallets

Revision ID: dd2b0b5cad52
Revises: f9996003f19b
Create Date: 2023-07-16 00:02:00.312973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd2b0b5cad52'
down_revision = 'f9996003f19b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=42), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spenders',
    sa.Column('spender_id', sa.Integer(), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spender_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spenders')
    op.drop_table('wallet')
    # ### end Alembic commands ###