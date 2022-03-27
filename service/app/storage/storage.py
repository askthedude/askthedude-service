from typing import Optional

from sqlalchemy.orm import Session
from .database import initialize_storage_development_mode
from .entity import User, Project, Technology


class Storage():
    def __init__(self):
        initialize_storage_development_mode()

    def get_uset_with_id(self, id: int, session: Session) -> Optional[User]:
        return session.query(User).filter(User.id == id).first()
