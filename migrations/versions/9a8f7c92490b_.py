"""empty message

Revision ID: 9a8f7c92490b
Revises: ed898b5853eb
Create Date: 2021-07-15 23:11:56.646311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a8f7c92490b'
down_revision = 'ed898b5853eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_datetime', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('to_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['to_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_creation_datetime'), 'post', ['creation_datetime'], unique=False)
    op.create_table('wall',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('wall_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['wall_id'], ['wall.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('wall')
    op.drop_index(op.f('ix_post_creation_datetime'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###