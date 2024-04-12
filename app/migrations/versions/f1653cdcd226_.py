"""empty message

Revision ID: f1653cdcd226
Revises: f03ccc129636
Create Date: 2024-04-12 09:56:20.249273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1653cdcd226'
down_revision = 'f03ccc129636'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    # ### end Alembic commands ###
