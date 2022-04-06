from typing import Optional, List
from dependencies.dependencies import storage, UserFilter
from dependencies.dependencies import PostUser, GetUser, PostRole
from storage.database import new_session


async def add_new_user(user: PostUser) -> Optional[GetUser]:
    session = new_session()
    try:
        is_present = await _is_user_with_email_present(user.email, session)
        print(is_present)
        if is_present:
            return None
        res = storage.add_user_entity(user, session)
        await session.flush()
        for role_id in user.role_ids:
            storage.add_user_role_entity(res.id, role_id, session)
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


async def get_user_profile_with_id(id: int) -> Optional[GetUser]:
    session = new_session()
    try:
        user = await storage.get_uset_with_id(id, session)
        if user:
            return GetUser(id=user.id, name=user.name, username=user.username, email=user.email, is_active=user.is_active,
                           github_url=user.github_url, linkedin_url=user.linkedin_url)
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        await session.close()


async def _is_user_with_email_present(email: str, session) -> bool:
    try:
        user = await storage.get_uset_with_email(email, session)
        return user is not None
    except Exception as e:
        print(e)
        return False
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