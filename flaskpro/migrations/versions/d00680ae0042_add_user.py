"""add user

Revision ID: d00680ae0042
Revises: 7d51c1360e01
Create Date: 2019-03-15 21:20:55.266376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd00680ae0042'
down_revision = '7d51c1360e01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick_name', sa.String(length=30), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('mobile', sa.String(length=11), nullable=True),
    sa.Column('image_url', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
