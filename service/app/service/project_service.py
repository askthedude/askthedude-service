from typing import Optional, List
from web.dto.dto import PostProject, \
    GetProject, ProjectFilter, PostStatistics, ProjectSubscriptionData
from service.domain.domain import PartialProjectData, TechnologyData, \
    CompleteProjectData, StatisticsData, UserData, ProjectSubscription

import storage.facade.project_storage_facade as project_facade


async def add_new_project(project: PostProject, user_id: int) -> Optional[GetProject]:
    result = await project_facade.add_new_project(project, user_id)
    return result


async def search_projects(project_filter: ProjectFilter) -> List[PartialProjectData]:
    result = []
    projects = await project_facade.filter_projects(project_filter)
    for project in projects:
        techs = [TechnologyData(tech.technology.id, tech.technology.name, tech.technology.is_hot, tech.technology.resource_url) for tech in project.Project.technologies]
        users = [user.user.username for user in project.Project.users]
        result.append(PartialProjectData(project.Project.title, project.Project.description, project.Project.stars, project.Project.is_active, project.Project.id, project.Project.url, project.Project.start_date, techs, users))
    return result


async def get_project_by_id(id: int):
    project = await project_facade.get_project_by_id(id)
    technologies = [TechnologyData(tech.technology.id, tech.technology.name, tech.technology.is_hot, tech.technology.resource_url) for tech in project.Project.technologies]
    users = [UserData(user.user.id, user.user.username, user.user.email, user.user.github_url, user.user.name, user.user.is_active, user.user.linkedin_url) for user in project.Project.users]
    sample_stats = project.Project.statistics[0]
    stats = StatisticsData(sample_stats.id, sample_stats.number_of_interested, sample_stats.subscriptions, sample_stats.seen_frequency)
    result = CompleteProjectData(project.Project.title, project.Project.description, project.Project.stars,
                                 project.Project.is_active, project.Project.id, project.Project.url,
                                 project.Project.start_date, technologies, users, stats)
    return result


async def post_project_statistics(id:int, stats: PostStatistics):
    if stats.delta_subscriptions < 0 or stats.delta_seen_frequency < 0 or stats.delta_number_of_interested < 0:
        return None
    new_projects_stats = await project_facade.update_project_stats(id, stats)
    sample_stats = new_projects_stats.ProjectStatistics
    res = StatisticsData(sample_stats.id, sample_stats.number_of_interested, sample_stats.subscriptions, sample_stats.seen_frequency)
    return res


async def add_new_subscription_for_project(subscription: ProjectSubscriptionData):
    if subscription.email is None or subscription.email == "" or subscription.project_id is None:
        return None
    new_subscription = await project_facade.add_new_subscription_project(subscription)
    if new_subscription is None:
        return None
    result = ProjectSubscriptionData(project_id=new_subscription.project_id, email=new_subscription.email)
    return result