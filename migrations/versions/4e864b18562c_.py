"""empty message

Revision ID: 4e864b18562c
Revises: 53fffefa353c
Create Date: 2024-12-24 07:49:45.231832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e864b18562c'
down_revision = '53fffefa353c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('teacher_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('teacher_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###