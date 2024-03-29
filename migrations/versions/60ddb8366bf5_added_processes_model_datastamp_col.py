"""added processes model datastamp col

Revision ID: 60ddb8366bf5
Revises: c7b8de37696b
Create Date: 2024-03-02 08:56:37.136067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60ddb8366bf5'
down_revision = 'c7b8de37696b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=False))
        batch_op.alter_column('pid',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('cpu_percent',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('memory_percent',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('cmdline',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('num_threads',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('create_time',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('num_fds',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processes', schema=None) as batch_op:
        batch_op.alter_column('num_fds',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('create_time',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('num_threads',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('cmdline',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('memory_percent',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('cpu_percent',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('pid',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
