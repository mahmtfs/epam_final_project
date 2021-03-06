"""Request model fix: department_id is no longer a foreign key

Revision ID: 2748e5daed1a
Revises: f55b98ada5de
Create Date: 2021-11-20 20:37:49.548773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2748e5daed1a'
down_revision = 'f55b98ada5de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('request_ibfk_1', 'request', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('request_ibfk_1', 'request', 'department', ['change_department_id'], ['id'])
    # ### end Alembic commands ###
