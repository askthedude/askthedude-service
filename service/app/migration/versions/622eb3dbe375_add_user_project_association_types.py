"""add user project association types

Revision ID: 622eb3dbe375
Revises: 3c3fbeebaeab
Create Date: 2022-04-04 20:52:24.451525

"""
from alembic import op
from sqlalchemy import orm
from storage.entity import UserProjectAssociationType, Role

# revision identifiers, used by Alembic.
revision = '622eb3dbe375'
down_revision = '3c3fbeebaeab'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    try:
        project_admin = UserProjectAssociationType(title="ADMIN")
        project_contributor = UserProjectAssociationType(title="CONTRIBUTOR")
        user = Role(title="USER")
        admin = Role(title="GLOBAL_ADMIN")
        session.add(project_admin)
        session.add(project_contributor)
        session.add(user)
        session.add(admin)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    try:
        session.query(UserProjectAssociationType)\
            .filter(UserProjectAssociationType.title == "ADMIN" or UserProjectAssociationType.title == "CONTRIBUTOR")\
            .delete()
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()
