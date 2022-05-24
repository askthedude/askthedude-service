import json
from typing import Optional, List

from service.exceptions.exceptions import ValidationException, ResourceNotFoundException
from service.validation.validation import validate_new_project, ValidationResult, validate_project_subscription, \
    validate_project_statistics, validate_comment_for_project
from utils.mappers import get_comments_tree
from web.dto.dto import PostProject, \
    GetProject, ProjectFilter, PostStatistics, ProjectSubscriptionData, AddCommentDto
from service.domain.domain import PartialProjectData, TechnologyData, \
    CompleteProjectData, StatisticsData, UserData, CommentData

import storage.facade.project_storage_facade as project_facade


async def add_new_project(project: PostProject, user_id: int) -> Optional[GetProject]:
    validation_res: ValidationResult = await validate_new_project(project)
    if validation_res.valid:
        return await project_facade.add_new_project(project, user_id)
    else:
        raise ValidationException("Add new project validation failed", validation_res.validationMessages)


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
    if project is None:
        raise ResourceNotFoundException("Couldn't find resource", f"Couldn't find project with id of {id}.")
    technologies = [TechnologyData(tech.technology.id, tech.technology.name, tech.technology.is_hot, tech.technology.resource_url) for tech in project.Project.technologies]
    users = [UserData(user.user.id, user.user.username, user.user.email, user.user.github_url, user.user.name, user.user.is_active, user.user.linkedin_url) for user in project.Project.users]
    sample_stats = project.Project.statistics[0]
    stats = StatisticsData(sample_stats.id, sample_stats.number_of_interested, sample_stats.subscriptions, sample_stats.seen_frequency)
    # new_comments = [comment.as_dict() for comment in project.Project.comments]
    # No nested comments supported yet, neet to look at this flow one more time.
    nested_comment_tree = get_comments_tree(project.Project.comments)
    result = CompleteProjectData(project.Project.title, project.Project.description, project.Project.stars,
                                 project.Project.is_active, project.Project.id, project.Project.url,
                                 project.Project.start_date, technologies, users, stats, nested_comment_tree)
    return result


async def post_project_statistics(id: int, stats: PostStatistics):
    validation_res: ValidationResult = validate_project_statistics(stats)
    if validation_res.valid:
        new_projects_stats = await project_facade.update_project_stats(id, stats)
        sample_stats = new_projects_stats.ProjectStatistics
        res = StatisticsData(sample_stats.id, sample_stats.number_of_interested, sample_stats.subscriptions,
                             sample_stats.seen_frequency)
        return res
    else:
        raise ValidationException("Project statistics input not valid", validation_res.validationMessages)


async def add_new_subscription_for_project(subscription: ProjectSubscriptionData):
    validation_result: ValidationResult = await validate_project_subscription(subscription)
    if validation_result.valid:
        new_subscription = await project_facade.add_new_subscription_project(subscription)
        result = ProjectSubscriptionData(project_id=new_subscription.project_id, email=new_subscription.email)
        return result
    else:
        raise ValidationException("Project subscription validation failed", validation_result.validationMessages)


async def add_comment_to_project(comment: AddCommentDto):
    validation_result: ValidationResult = await validate_comment_for_project(comment)
    if validation_result.valid:
        result = await project_facade.add_comment_for_project(comment)
        # result_comment = GetcommentDto(id=result.id)
        return result
    else:
        raise ValidationException("Comment validation failed", validation_result.validationMessages)