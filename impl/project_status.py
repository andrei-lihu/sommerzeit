#!/usr/bin/env python

from skill_sdk import skill, Response
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import get_jira_account, get_jira_tasks, many_or_none_message, get_project_users, format_enumeration


@skill.intent_handler("TEAM_24_PROJECT_STATUS")
def team_24_project_status_handler() -> Response:
    """ TEAM_24_PROJECT_STATUS handler

    :return:
    """

    urgent_q = 'project = {project} AND status IN ("To Do") and priority in (Highest)'.\
        format(project=config.get('jira', 'project'))

    overdue_q = 'project = {project} AND duedate < Now() and status in ("In Progress", "To Do")'.\
        format(project=config.get('jira', 'project'))

    jira_account = get_jira_account()
    todo_tasks, todo_tasks_count_msg = get_jira_tasks(get_board_query("To Do"), jira_account)
    inprogress_tasks, inprogress_tasks_count_msg = get_jira_tasks(get_board_query("In Progress"), jira_account)
    done_tasks, done_tasks_count_msg = get_jira_tasks(get_board_query("Done"), jira_account)
    urgent_tasks, urgent_tasks_count_msg = get_jira_tasks(urgent_q, jira_account)
    overdue_tasks, overdue_tasks_count_msg = get_jira_tasks(overdue_q, jira_account)
    idle_users = get_idle_users(jira_account)

    msg = _("SPRINT_STATUS",
             project=config.get('jira', 'project'),
             todos=todo_tasks_count_msg,
             inprogress=inprogress_tasks_count_msg,
             done=done_tasks_count_msg)

    msg += " " + _("PROJECT_STATUS_INTRO",
            project=config.get('jira', 'project'),
            urgent_tasks=urgent_tasks_count_msg,
            overdue_tasks=overdue_tasks_count_msg)

    if len(idle_users) > 0:
        verb = _("ARE")
        if len(idle_users) == 1:
            verb = _("IS")
        user_str = format_enumeration(idle_users)
        msg_idle = " " + _("IDLE_USERS", users=user_str, verb=verb)
        msg += msg_idle

    response = Response(msg)
    return response


def get_board_query(state):
    return 'project = {project} AND status IN ("{state}") AND Sprint = "{sprint}" '. \
        format(project=config.get('jira', 'project'), sprint=config.get('jira', 'sprint'), state=state)


def get_idle_users(jira_account):
    users = get_project_users()
    idle_q = "project = {project} AND assignee = '{user}' AND status IN ('In Progress') ORDER BY issuekey"
    idle_users = []
    for user in users:
        idle_q_user = idle_q.format(project=config.get('jira', 'project'), user=user)
        in_progress_tasks, in_progress_tasks_count_msg = get_jira_tasks(idle_q_user, jira_account)
        if in_progress_tasks_count_msg == _("NONE"):
            idle_users.append(user)
    return idle_users
