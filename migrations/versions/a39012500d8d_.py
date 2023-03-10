"""empty message

Revision ID: a39012500d8d
Revises: 2397a8867b44
Create Date: 2023-02-09 15:50:55.712510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a39012500d8d'
down_revision = '2397a8867b44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
