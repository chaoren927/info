"""add lan 

Revision ID: c8318253539e
Revises: 3f1a8fb48004
Create Date: 2019-03-18 15:48:14.941470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8318253539e'
down_revision = '3f1a8fb48004'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('joy', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('language', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'language')
    op.drop_column('user', 'joy')
    # ### end Alembic commands ###