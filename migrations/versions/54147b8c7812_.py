"""empty message

Revision ID: 54147b8c7812
Revises: 3b021305fbc3
Create Date: 2023-09-04 19:35:02.303136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54147b8c7812'
down_revision = '3b021305fbc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('path', sa.String(length=2048), nullable=True),
    sa.Column('is_empty', sa.Boolean(), nullable=True),
    sa.Column('replacement', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wall',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=42), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('erc360',
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('sin_rad_lat', sa.Float(), nullable=True),
    sa.Column('cos_rad_lat', sa.Float(), nullable=True),
    sa.Column('rad_lng', sa.Float(), nullable=True),
    sa.Column('show_location', sa.Boolean(), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('address', sa.String(length=42), nullable=True),
    sa.Column('block', sa.Integer(), nullable=True),
    sa.Column('current_clock', sa.Integer(), nullable=True),
    sa.Column('total_amount', sa.Integer(), nullable=True),
    sa.Column('events_last_updated_at', sa.Integer(), nullable=True),
    sa.Column('shards_last_updated_at', sa.Integer(), nullable=True),
    sa.Column('bank_exchanges_last_updated_at', sa.Integer(), nullable=True),
    sa.Column('dividend_claims_last_updated_at', sa.Integer(), nullable=True),
    sa.Column('referendum_votes_last_updated_at', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('handle', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['photo_id'], ['photo.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('erc360', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_erc360_handle'), ['handle'], unique=True)

    op.create_table('user',
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('sin_rad_lat', sa.Float(), nullable=True),
    sa.Column('cos_rad_lat', sa.Float(), nullable=True),
    sa.Column('rad_lng', sa.Float(), nullable=True),
    sa.Column('show_location', sa.Boolean(), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_datetime', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('is_activated', sa.Boolean(), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('bio', sa.String(length=160), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.Column('wall_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photo.id'], ),
    sa.ForeignKeyConstraint(['wall_id'], ['wall.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_creation_datetime'), ['creation_datetime'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('erc360_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.Column('block_hash', sa.String(length=66), nullable=True),
    sa.Column('transaction_hash', sa.String(length=66), nullable=True),
    sa.Column('log_index', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['erc360_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('associates',
    sa.Column('left_id', sa.Integer(), nullable=True),
    sa.Column('right_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['left_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['user.id'], )
    )
    op.create_table('conversations',
    sa.Column('conversation_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('dividend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('erc360_id', sa.Integer(), nullable=True),
    sa.Column('clock', sa.BigInteger(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('token_address', sa.String(length=42), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('residual', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['erc360_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('erc360_token_id',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('erc360_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('identity', sa.LargeBinary(length=32), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('creation_timestamp', sa.Integer(), nullable=True),
    sa.Column('expiration_timestamp', sa.Integer(), nullable=True),
    sa.Column('creation_clock', sa.BigInteger(), nullable=True),
    sa.Column('expiration_clock', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['erc360_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_id'], ['wallet.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback',
    sa.Column('creation_datetime', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('to_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_id'], ['feedback.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_feedback_creation_datetime'), ['creation_datetime'], unique=False)

    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('medium',
    sa.Column('creation_datetime', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('with_quote', sa.Boolean(), nullable=True),
    sa.Column('reply_to_id', sa.Integer(), nullable=True),
    sa.Column('quote_to_id', sa.Integer(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['channel_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['quote_to_id'], ['medium.id'], ),
    sa.ForeignKeyConstraint(['reply_to_id'], ['medium.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('medium', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_medium_creation_datetime'), ['creation_datetime'], unique=False)

    op.create_table('membership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_datetime', sa.DateTime(), nullable=True),
    sa.Column('seen', sa.Boolean(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('conversation_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_creation_datetime'), ['creation_datetime'], unique=False)

    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seen', sa.Boolean(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notification_timestamp'), ['timestamp'], unique=False)

    op.create_table('permit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('erc360_id', sa.Integer(), nullable=True),
    sa.Column('bytes', sa.LargeBinary(length=32), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['erc360_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_id'], ['permit.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referendum',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('erc360_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('implemented', sa.Boolean(), nullable=True),
    sa.Column('viable_amount', sa.Integer(), nullable=True),
    sa.Column('cast_amount', sa.Integer(), nullable=True),
    sa.Column('in_favor_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['erc360_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('skill', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_skill_title'), ['title'], unique=False)

    op.create_table('spenders',
    sa.Column('spender_id', sa.Integer(), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spender_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], )
    )
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('erc360_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('permit_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['erc360_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['permit_id'], ['permit.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dividend_claim',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dividend_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('erc360_token_id_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dividend_id'], ['dividend.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('erc360_to_user_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('notification_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['notification_id'], ['notification.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('erc360_to_user_request', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_erc360_to_user_request_type'), ['type'], unique=False)

    op.create_table('feedback_downvote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feedback_id', sa.Integer(), nullable=True),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ),
    sa.ForeignKeyConstraint(['voter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback_upvote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feedback_id', sa.Integer(), nullable=True),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ),
    sa.ForeignKeyConstraint(['voter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media',
    sa.Column('media_id', sa.Integer(), nullable=True),
    sa.Column('wall_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['media_id'], ['medium.id'], ),
    sa.ForeignKeyConstraint(['wall_id'], ['wall.id'], )
    )
    op.create_table('medium_downvote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['voter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medium_heart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medium_id', sa.Integer(), nullable=True),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medium_id'], ['medium.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['voter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referendum_proposal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referendum_id', sa.Integer(), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('sig', sa.LargeBinary(length=4), nullable=True),
    sa.Column('args', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['referendum_id'], ['referendum.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referendum_vote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referendum_id', sa.Integer(), nullable=True),
    sa.Column('erc360_token_id_id', sa.Integer(), nullable=True),
    sa.Column('in_favor', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['referendum_id'], ['referendum.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_erc360_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('notification_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['notification_id'], ['notification.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['erc360.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_to_erc360_request', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_to_erc360_request_type'), ['type'], unique=False)

    op.create_table('user_to_user_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('notification_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['notification_id'], ['notification.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_to_user_request', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_to_user_request_type'), ['type'], unique=False)

    op.create_table('token_amount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('token_address', sa.String(length=42), nullable=True),
    sa.Column('value', sa.Numeric(precision=78), nullable=True),
    sa.Column('sender_address', sa.String(length=42), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['bank.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token_amount')
    with op.batch_alter_table('user_to_user_request', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_to_user_request_type'))

    op.drop_table('user_to_user_request')
    with op.batch_alter_table('user_to_erc360_request', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_to_erc360_request_type'))

    op.drop_table('user_to_erc360_request')
    op.drop_table('referendum_vote')
    op.drop_table('referendum_proposal')
    op.drop_table('medium_heart')
    op.drop_table('medium_downvote')
    op.drop_table('media')
    op.drop_table('feedback_upvote')
    op.drop_table('feedback_downvote')
    with op.batch_alter_table('erc360_to_user_request', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_erc360_to_user_request_type'))

    op.drop_table('erc360_to_user_request')
    op.drop_table('dividend_claim')
    op.drop_table('bank')
    op.drop_table('spenders')
    with op.batch_alter_table('skill', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_skill_title'))

    op.drop_table('skill')
    op.drop_table('referendum')
    op.drop_table('permit')
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notification_timestamp'))

    op.drop_table('notification')
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_creation_datetime'))

    op.drop_table('message')
    op.drop_table('membership')
    with op.batch_alter_table('medium', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_medium_creation_datetime'))

    op.drop_table('medium')
    op.drop_table('followers')
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_feedback_creation_datetime'))

    op.drop_table('feedback')
    op.drop_table('erc360_token_id')
    op.drop_table('dividend')
    op.drop_table('conversations')
    op.drop_table('associates')
    op.drop_table('action')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_creation_datetime'))

    op.drop_table('user')
    with op.batch_alter_table('erc360', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_erc360_handle'))

    op.drop_table('erc360')
    op.drop_table('wallet')
    op.drop_table('wall')
    op.drop_table('photo')
    op.drop_table('group')
    op.drop_table('conversation')
    # ### end Alembic commands ###