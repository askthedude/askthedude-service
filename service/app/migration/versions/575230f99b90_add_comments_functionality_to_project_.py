"""Add comments functionality to project pages

Revision ID: 575230f99b90
Revises: e8679bd50ed7
Create Date: 2022-05-10 16:04:01.859257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '575230f99b90'
down_revision = 'e8679bd50ed7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('comment',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('project_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), default=None),
                    sa.Column('parent_comment_id', sa.Integer(), default=None),
                    sa.Column('content', sa.String()),
                    sa.Column('created_timestamp', sa.String()),
                    sa.Column('edited_timestamp', sa.String()),
                    sa.Column('active', sa.Boolean(), nullable=False, default=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
                    sa.ForeignKeyConstraint(['project_id'], ['project.id']),
                    sa.ForeignKeyConstraint(['parent_comment_id'], ['comment.id']),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('comment')
