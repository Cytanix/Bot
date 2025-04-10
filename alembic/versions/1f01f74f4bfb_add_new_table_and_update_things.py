"""add new table and update things

Revision ID: 1f01f74f4bfb
Revises: 3bc922095042
Create Date: 2025-03-26 00:51:32.892498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f01f74f4bfb'
down_revision: Union[str, None] = '3bc922095042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reg_roles',
    sa.Column('guild_id', sa.BigInteger(), nullable=False),
    sa.Column('registered', sa.BigInteger(), nullable=True),
    sa.Column('mention_mention', sa.BigInteger(), nullable=True),
    sa.Column('mention_no_mention', sa.BigInteger(), nullable=True),
    sa.Column('dms_allowed', sa.BigInteger(), nullable=True),
    sa.Column('dms_not_allowed', sa.BigInteger(), nullable=True),
    sa.Column('dms_ask', sa.BigInteger(), nullable=True),
    sa.Column('gender_male', sa.BigInteger(), nullable=True),
    sa.Column('gender_female', sa.BigInteger(), nullable=True),
    sa.Column('gender_genderfluid', sa.BigInteger(), nullable=True),
    sa.Column('gender_agender', sa.BigInteger(), nullable=True),
    sa.Column('gender_non_binary', sa.BigInteger(), nullable=True),
    sa.Column('gender_transgender', sa.BigInteger(), nullable=True),
    sa.Column('gender_trans_male', sa.BigInteger(), nullable=True),
    sa.Column('gender_trans_female', sa.BigInteger(), nullable=True),
    sa.Column('relationship_taken', sa.BigInteger(), nullable=True),
    sa.Column('relationship_single', sa.BigInteger(), nullable=True),
    sa.Column('relationship_single_seeking', sa.BigInteger(), nullable=True),
    sa.Column('relationship_single_not', sa.BigInteger(), nullable=True),
    sa.Column('relationship_rather_not', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_asexual', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_bisexual', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_gay', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_lesbian', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_pansexual', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_aromantic', sa.BigInteger(), nullable=True),
    sa.Column('sexuality_rather_not', sa.BigInteger(), nullable=True),
    sa.Column('position_dominant', sa.BigInteger(), nullable=True),
    sa.Column('position_submissive', sa.BigInteger(), nullable=True),
    sa.Column('position_switch', sa.BigInteger(), nullable=True),
    sa.Column('position_rather_not', sa.BigInteger(), nullable=True),
    sa.Column('position_neither', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['guild_id'], ['logs.guild_id'], ),
    sa.PrimaryKeyConstraint('guild_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reg_roles')
    # ### end Alembic commands ###
