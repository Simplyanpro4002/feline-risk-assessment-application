"""Add scoring columns

Revision ID: 19b57977a8a7
Revises: 
Create Date: 2024-03-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19b57977a8a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns with default values
    op.add_column('result', sa.Column('raw_score', sa.Integer(), server_default='0', nullable=False))
    op.add_column('result', sa.Column('standard_score', sa.Float(), server_default='0.0', nullable=False))
    op.add_column('result', sa.Column('risk_group', sa.Integer(), server_default='1', nullable=False))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=128),
               nullable=True)
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # Remove the new columns
    op.drop_column('result', 'raw_score')
    op.drop_column('result', 'standard_score')
    op.drop_column('result', 'risk_group')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=256),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
