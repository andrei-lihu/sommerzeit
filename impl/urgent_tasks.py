#!/usr/bin/env python

from skill_sdk import skill, Response
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import get_jira_account, format_enumeration


@skill.intent_handler("TEAM_24_URGENT_TASKS")
def team_24_project_status_handler() -> Response:
    urgent_msg = _("NO_URGENT_TASKS")
    tasks = get_urgent_tasks()
    if len(tasks) > 0:
        urgent_msg = _("URGENT_TASKS_INTRO") + format_enumeration([_("URGENT_TASK", task=t[0], user=t[1]) for t in tasks]) + "."
    response = Response(urgent_msg)
    return response


def get_urgent_tasks():
    urgent_q = 'project = {project} AND status IN ("To Do") and priority in (Highest)'. \
        format(project=config.get('jira', 'project'))
    account = get_jira_account()
    q_res = account.jql(urgent_q)
    tasks = [(t['fields']['summary'], t['fields']['assignee']['displayName']) for t in q_res['issues']]
    return tasks
