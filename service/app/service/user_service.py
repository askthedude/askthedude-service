from dependencies.dependencies import storage
from web.user import PostUser, GetUser
from storage.database import new_session
import logging

logger = logging.getLogger("gunicorn.error")


def add_new_user(user: PostUser) -> GetUser:
    logger.info(user)
    session = new_session()
    user = storage.add_user(user, session)
    session.commit()
    session.refresh(user)
    return GetUser(id=user.id, username=user.username, name=user.name, email=user.email, is_active=user.is_active,
                   github_url=user.github_url, linkedin_url=user.linkedin_url)


def get_user_with_id(id: int) -> GetUser:
    session = new_session()
    user = storage.get_uset_with_id(id, session)
    logger.info(user)
    session.commit()
    return GetUser(id=user.id, name=user.name, username=user.username, email=user.email, is_active=user.is_active, github_url=user.github_url, linkedin_url=user.linkedin_url)
