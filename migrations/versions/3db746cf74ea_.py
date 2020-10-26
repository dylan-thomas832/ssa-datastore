"""empty message

Revision ID: 3db746cf74ea
Revises: 6b395bddb6d1
Create Date: 2020-10-26 02:36:43.833498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3db746cf74ea'
down_revision = '6b395bddb6d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'sensor', ['unique_id'])
    op.create_unique_constraint(None, 'target', ['unique_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'target', type_='unique')
    op.drop_constraint(None, 'sensor', type_='unique')
    # ### end Alembic commands ###
