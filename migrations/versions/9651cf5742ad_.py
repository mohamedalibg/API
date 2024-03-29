"""empty message

Revision ID: 9651cf5742ad
Revises: c6d4ee23a521
Create Date: 2024-01-16 21:06:43.626805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9651cf5742ad'
down_revision = 'c6d4ee23a521'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('call_duration', sa.Integer(), nullable=False),
    sa.Column('messages', sa.Integer(), nullable=False),
    sa.Column('data_usage', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    # ### end Alembic commands ###
