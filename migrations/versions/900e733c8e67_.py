"""empty message

Revision ID: 900e733c8e67
Revises: a9e54e8b6126
Create Date: 2021-04-26 16:42:26.929895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '900e733c8e67'
down_revision = 'a9e54e8b6126'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_notification_title', table_name='notification')
    op.drop_column('notification', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('title', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.create_index('ix_notification_title', 'notification', ['title'], unique=False)
    # ### end Alembic commands ###