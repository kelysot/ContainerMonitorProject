"""change models secound time

Revision ID: f23db4398984
Revises: 906fa1d2b5dd
Create Date: 2024-02-28 11:43:28.479315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f23db4398984'
down_revision = '906fa1d2b5dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('create_time',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('create_time',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
