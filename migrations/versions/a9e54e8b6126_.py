"""empty message

Revision ID: a9e54e8b6126
Revises: c2e609d10d20
Create Date: 2021-04-26 16:23:55.120691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e54e8b6126'
down_revision = 'c2e609d10d20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club_to_user_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['club.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_to_user_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['club.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_club_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['club.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_project_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['project.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_user_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('request')
    op.drop_constraint('notification_receiver_id_fkey', 'notification', type_='foreignkey')
    op.drop_column('notification', 'receiver_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('receiver_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('notification_receiver_id_fkey', 'notification', 'user', ['receiver_id'], ['id'])
    op.create_table('request',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], name='request_receiver_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], name='request_sender_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='request_pkey')
    )
    op.drop_table('user_to_user_request')
    op.drop_table('user_to_project_request')
    op.drop_table('user_to_club_request')
    op.drop_table('project_to_user_request')
    op.drop_table('club_to_user_request')
    # ### end Alembic commands ###