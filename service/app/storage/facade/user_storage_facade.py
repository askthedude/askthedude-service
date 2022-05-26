from service.domain.domain import UserTechnologyInterest
from service.exceptions.exceptions import ResourceConflictException
from web.dto.dto import UserFilter
from web.dto.dto import PostUser, GetUser, PostRole, AnonymousUserData
from storage.storage import storage
from storage.facade.transaction_manager import run_with_transaction


async def add_new_user(user: PostUser):
    async def work(session):
        is_present = await _is_user_with_email_username_present(user.email, user.username, session)
        if is_present:
            return None
        res = storage.add_user_entity(user, session)
        await session.flush()
        role = await storage.get_role_entity_with_title("USER", session)
        storage.add_user_role_entity(res.id, role.Role.id, session)
        return res
    res = await run_with_transaction(work, should_refresh=True)
    if res is None:
        return None
    return GetUser(id=res.id, username=res.username, name=res.name, email=res.email, is_active=res.is_active,
                   github_url=res.github_url, linkedin_url=res.linkedin_url)


async def _is_user_with_email_username_present(email: str, username: str, session) -> bool:
    async def work(session):
        user = await storage.get_uset_with_email(email, username, session)
        return user
    res = await run_with_transaction(work, session, False)
    return res is not None


async def get_user_profile_with_id(id: int):
    async def work(session):
        user = await storage.get_user_with_id(id, session)
        return user
    return await run_with_transaction(work)


async def get_user_profile_with_username(username: str):
    async def work(session):
        user = await storage.get_uset_with_username(username, session)
        return user
    return await run_with_transaction(work)


async def add_role(new_role: PostRole):
    async def work(session):
        role = await storage.get_role_with_title(new_role.title, session)
        if role is None:
            res = storage.add_role_entity(new_role, session)
            return res
        else:
            raise ResourceConflictException(f"role with title: {new_role.title} is already present")
    return await run_with_transaction(work)


async def filter_all_users(user_filter: UserFilter):
    async def work(session):
        res = await storage.filter_users(user_filter, session)
        return res
    return await run_with_transaction(work)


async def get_user_with_identifier_token(token: str):
    async def work(session):
        anonymous_user = await storage.get_user_with_identifier_token(token, session)
        return anonymous_user
    return await run_with_transaction(work)


async def add_anonymous_user(user: AnonymousUserData):
    async def work(session):
        anonymous_user = await storage.get_user_with_identifier_token(user.identifier_token, session)
        if anonymous_user is None:
            res = storage.add_anonymous_user(user, session)
            return res
        else:
            return anonymous_user
    return await run_with_transaction(work)


async def add_user_technology_interest(userTechnology: UserTechnologyInterest):
    async def work(session):
        res = storage.add_user_technology_interest(userTechnology, session)
        return res
    return await run_with_transaction(work)
