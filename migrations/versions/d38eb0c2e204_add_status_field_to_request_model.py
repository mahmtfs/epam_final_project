"""Add status field to Request model

Revision ID: d38eb0c2e204
Revises: 2748e5daed1a
Create Date: 2021-11-20 20:41:29.717106

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd38eb0c2e204'
down_revision = '2748e5daed1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('status', sa.Integer(), nullable=False))
    op.drop_column('request', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('request', 'status')
    # ### end Alembic commands ###