"""empty message

Revision ID: 99e04e87f7cc
Revises: 
Create Date: 2020-11-20 21:12:16.533104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99e04e87f7cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('picture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=25), nullable=True),
    sa.Column('path', sa.String(length=2048), nullable=True),
    sa.Column('replacement', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('location', sa.String(length=120), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('sin_rad_lat', sa.Float(), nullable=True),
    sa.Column('cos_rad_lat', sa.Float(), nullable=True),
    sa.Column('rad_lng', sa.Float(), nullable=True),
    sa.Column('profile_pic_id', sa.Integer(), nullable=True),
    sa.Column('cover_pic_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cover_pic_id'], ['picture.id'], ),
    sa.ForeignKeyConstraint(['profile_pic_id'], ['picture.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skill_title'), 'skill', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_skill_title'), table_name='skill')
    op.drop_table('skill')
    op.drop_table('followers')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('picture')
    # ### end Alembic commands ###