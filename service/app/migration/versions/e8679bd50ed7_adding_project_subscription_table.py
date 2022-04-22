"""adding project_subscription table

Revision ID: e8679bd50ed7
Revises: 622eb3dbe375
Create Date: 2022-04-22 15:32:45.957445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8679bd50ed7'
down_revision = '622eb3dbe375'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('project_subscription',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=False, default=True),
                    sa.Column('project_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['project_id'], ['project.id']),
                    sa.UniqueConstraint('project_id', 'email'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('project_subscription')
