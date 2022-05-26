from typing import Optional
from storage.facade.transaction_manager import run_with_transaction

from web.dto.dto import ProjectFilter, PostProject, \
    GetProject, PostTechnology, GetTechnology, PostStatistics, TechnologyFilter, \
    ProjectSubscriptionData
from storage.storage import storage


async def add_new_project(project: PostProject, user_id: int) -> Optional[GetProject]:
    async def work(session):
        proj = storage.add_project_entity(project, session)
        await session.flush()
        res = await storage.find_user_project_assoc_type_with_title("ADMIN", session)
        storage.add_project_user_relation(proj.id, user_id, res[0], session)
        for tech_id in project.technology_ids:
            storage.add_project_technology_relation(proj.id, tech_id, session)
        storage.add_blank_project_frequency_entity(proj.id, session)
        res = GetProject(id=proj.id, title=proj.title, description=proj.description, start_date=proj.start_date,
                         stars=proj.stars, github_url=proj.url, url=proj.url, is_active=proj.is_active, user_id=user_id,
                         technology_ids=project.technology_ids)
        return res
    return await run_with_transaction(work)


async def filter_projects(project_filter: ProjectFilter):
    async def work(session):
        projects = await storage.filter_projects(project_filter, session)
        return projects
    return await run_with_transaction(work)


async def add_new_technology(technology: PostTechnology) -> Optional[GetTechnology]:
    async def work(session):
        tech = storage.add_technology(technology, session)
        await session.refresh(tech)
        return tech
    return await run_with_transaction(work)


async def add_new_subscription_project(subscription: ProjectSubscriptionData):
    async def work(session):
        new_subscription = storage.add_subscription(subscription, session)
        await session.refresh(new_subscription)
        return new_subscription
    return await run_with_transaction(work)


async def get_project_by_id(id: int):
    async def work(session):
        res = await storage.get_project_by_id(id, session)
        return res
    return await run_with_transaction(work)


async def filter_technologies(tech_filter: TechnologyFilter):
    async def work(session):
        techs = await storage.filter_technologies(tech_filter.title, session)
        return techs
    return await run_with_transaction(work)


async def update_project_stats(id: int, stats: PostStatistics):
    async def work(session):
        techs = await storage.update_project_stats(id, stats, session)
        return techs
    return await run_with_transaction(work)


async def add_comment_for_project(comment):
    async def work(session):
        res = storage.add_comment_to_project(comment, session)
        await session.refresh(res)
        return res
    return await run_with_transaction(work)