"""units.status

Revision ID: f0f76332534c
Revises: 472e5c45ac28
Create Date: 2025-01-03 16:45:05.660726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0f76332534c'
down_revision = '472e5c45ac28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('units', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('units', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###