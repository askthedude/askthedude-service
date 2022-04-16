from web.dto.dto import UserFilter
from web.dto.dto import PostUser, GetUser, PostRole
from storage.database import new_session
from storage.storage import storage


async def add_new_user(user: PostUser):
    session = new_session()
    try:
        is_present = await _is_user_with_email_username_present(user.email, user.username, session)
        if is_present:
            return None
        res = storage.add_user_entity(user, session)
        await session.flush()
        role = await storage.get_role_entity_with_title("USER", session)
        storage.add_user_role_entity(res.id, role.Role.id, session)
        await session.commit()
        await session.refresh(res)
        return GetUser(id=res.id, username=res.username, name=res.name, email=res.email, is_active=res.is_active,
                       github_url=res.github_url, linkedin_url=res.linkedin_url)
    except Exception as e:
        print(e)
        await session.rollback()
        return None
    finally:
        await session.close()


async def _is_user_with_email_username_present(email: str, username: str, session) -> bool:
    try:
        user = await storage.get_uset_with_email(email, username, session)
        return user is not None
    except Exception as e:
        print(e)
        return False
    finally:
        await session.close()


async def get_user_profile_with_id(id: int):
    session = new_session()
    try:
        user = await storage.get_user_with_id(id, session)
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        await session.close()


async def get_user_profile_with_username(username: str):
    session = new_session()
    try:
        user = await storage.get_uset_with_username(username, session)
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        await session.close()



async def add_role(new_role: PostRole):
    session = new_session()
    try:
        role = await storage.get_role_with_title(new_role.title, session)
        if role is None:
            res = storage.add_role_entity(new_role, session)
            await session.commit()
            await session.refresh(res)
            return res
        else:
            return None
    except Exception as e:
        print(e)
        await session.rollback()
        return None
    finally:
        await session.close()


async def filter_all_users(user_filter: UserFilter):
    session = new_session()
    try:
        res = await storage.filter_users(user_filter, session)
        return res
    except Exception as e:
        print(e)
        return []
    finally:
        await session.close()
