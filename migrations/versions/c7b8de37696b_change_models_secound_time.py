"""change models secound time

Revision ID: c7b8de37696b
Revises: 2cfec4fb0f5f
Create Date: 2024-02-28 11:52:31.206409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7b8de37696b'
down_revision = '2cfec4fb0f5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('pid',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('cpu_percent',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('memory_percent',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('cmdline',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('num_threads',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('create_time',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('num_fds',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('num_fds',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('create_time',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('num_threads',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('cmdline',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('memory_percent',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('cpu_percent',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('pid',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
