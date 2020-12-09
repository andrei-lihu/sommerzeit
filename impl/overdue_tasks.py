#!/usr/bin/env python
from datetime import datetime
from dateutil.parser import parse

from skill_sdk import skill, Response
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import get_jira_account, get_jira_tasks, many_or_none_message, get_project_users, format_enumeration, \
    get_jira_tasks_with_due_dates


@skill.intent_handler("TEAM_24_OVERDUE_TASKS")
def team_24_project_status_handler() -> Response:
    overdue_q = 'project = {project} AND assignee = "{user}" AND duedate < Now() and status in ("In Progress", "To Do")'
    jira_account = get_jira_account()
    users = get_project_users()
    overdue_msg = ""
    for user in users:
        overdue_q_user = overdue_q.format(project=config.get('jira', 'project'), user=user)
        overdue_tasks = get_jira_tasks_with_due_dates(overdue_q_user, jira_account)
        overdue_tasks_count = len(overdue_tasks)
        if overdue_tasks_count > 0:
            overdue_msg += user + _("ASSIGNED") + " "
            for idx, tpl in enumerate(overdue_tasks):
                overdue_msg += _("OVERDUE_TASK", task=tpl[0], days=(datetime.now() - parse(tpl[1])).days)
                overdue_msg += ", " if idx != overdue_tasks_count - 1 else "."

    if overdue_msg == "":
        overdue_msg = _("NO_OVERDUE_TASKS")

    response = Response(overdue_msg)
    return response
