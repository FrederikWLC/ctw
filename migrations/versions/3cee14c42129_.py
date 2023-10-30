"""empty message

Revision ID: 3cee14c42129
Revises: ad3c0590b54e
Create Date: 2023-09-18 16:19:09.324631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cee14c42129'
down_revision = 'ad3c0590b54e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permits',
    sa.Column('permit_id', sa.Integer(), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permit_id'], ['permit.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], )
    )
    op.drop_table('holders')
    with op.batch_alter_table('erc360_token_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wallet_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('erc360_token_id_owner_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'wallet', ['wallet_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('owner_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('erc360_token_id', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('erc360_token_id_owner_id_fkey', 'wallet', ['owner_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('wallet_id')

    op.create_table('holders',
    sa.Column('holder_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('permit_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['holder_id'], ['wallet.id'], name='holders_holder_id_fkey'),
    sa.ForeignKeyConstraint(['permit_id'], ['permit.id'], name='holders_permit_id_fkey')
    )
    op.drop_table('permits')
    # ### end Alembic commands ###