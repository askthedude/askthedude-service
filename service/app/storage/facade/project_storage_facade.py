from dependencies.dependencies import ProjectFilter, storage
from storage.database import new_session


async def filter_projects(project_filter: ProjectFilter):
    session = new_session()
    try:
        projects = await storage.filter_projects(project_filter, session)
        return projects
    except Exception as e:
        print(e)
        return []
    finally:
        await session.close()
