#!/usr/bin/env python
from datetime import datetime
from dateutil.parser import parse

from skill_sdk import skill, Response, ask, tell
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import get_backlog, get_jira_account, format_enumeration, get_jira_tasks, clarify_user, \
    get_jira_tasks_with_due_dates


@skill.intent_handler("TEAM_24_COWORKER_STATUS")
def team_24_call_handler(username: str) -> Response:
    """ TEAM_24_COWORKER_STATUS handler

    :param username: str
    :return:
    """

    user = clarify_user(username)

    jira_account = get_jira_account()
    todo_tasks, todo_tasks_count_msg = get_jira_tasks(get_user_board_query("To Do", user), jira_account)
    inprogress_tasks, inprogress_tasks_count_msg = get_jira_tasks(get_user_board_query("In Progress", user),
                                                                  jira_account)
    done_tasks, done_tasks_count_msg = get_jira_tasks(get_user_board_query("Done", user), jira_account)

    msg = _("COWORKER_STATUS",
            username=username,
            todos=todo_tasks_count_msg,
            inprogress=inprogress_tasks_count_msg,
            done=done_tasks_count_msg)

    if inprogress_tasks_count_msg != _("NONE"):
        msg += " " + _("COWORKER_INPROGRESS", username=user, tasks=format_enumeration(inprogress_tasks))

    urgent_q = 'project = {project} AND assignee = "{username}" AND status IN ("To Do") and priority in (Highest)'. \
        format(project=config.get('jira', 'project'), username=user)

    overdue_q = 'project = {project} AND assignee = "{username}" AND duedate < Now() and status in ("In Progress", ' \
                '"To Do")'. \
        format(project=config.get('jira', 'project'), username=user)

    urgent_tasks, urgent_tasks_count_msg = get_jira_tasks(urgent_q, jira_account)
    if urgent_tasks_count_msg != _("NONE"):
        msg += _("COWORKER_URGENT", username=user, tasks=format_enumeration(urgent_tasks)) + "."

    overdue_tasks = get_jira_tasks_with_due_dates(overdue_q, jira_account)
    overdue_tasks_count = len(overdue_tasks)
    if overdue_tasks_count > 0:
        msg += _("COWORKER_OVERDUE", username=user)
        for idx, tpl in enumerate(overdue_tasks):
            msg += _("OVERDUE_TASK", task=tpl[0], days=(datetime.now() - parse(tpl[1])).days)
            msg += ", " if idx != overdue_tasks_count - 1 else "."

    no_tasks_q = "project = {project} AND assignee = '{user}' AND status IN ('In Progress', 'To Do') ORDER BY issuekey".format(
        project=config.get('jira', 'project'), user=user)
    tasks, tasks_count_msg = get_jira_tasks(no_tasks_q, jira_account)
    if len(tasks) == 0:
        msg += " " + _("COWORKER_EMPTY")
    else:
        idle_tasks_q = "project = {project} AND assignee = '{user}' AND status IN ('In Progress') ORDER BY " \
                       "issuekey".format(project=config.get('jira', 'project'), user=user)
        idle_tasks, idle_tasks_count_msg = get_jira_tasks(idle_tasks_q, jira_account)
        if len(idle_tasks) == 0:
            msg += " " + _("COWORKER_IDLE")

    response = Response(msg)
    return response


def get_user_board_query(state, username):
    return 'project = {project} AND assignee = "{username}" AND status IN ("{state}") AND Sprint = "{sprint}" '. \
        format(project=config.get('jira', 'project'), username=username, sprint=config.get('jira', 'sprint'),
               state=state)
