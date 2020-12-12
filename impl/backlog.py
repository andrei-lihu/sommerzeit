#!/usr/bin/env python

from skill_sdk import skill, Response, ask, tell
from skill_sdk.l10n import _

from impl.utils import get_backlog, get_jira_account, format_enumeration


@skill.intent_handler("TEAM_24_BACKLOG")
def team_24_call_handler() -> Response:
    """ TEAM_24_CALL handler
    :return:
    """

    jira_account = get_jira_account()
    tasks, tasks_count_msg = get_backlog(jira_account)
    if tasks_count_msg == _("NONE"):
        return _("NO_BACKLOG")

    msg = _("BACKLOG_INTRO")
    msg += format_enumeration(tasks) + "."

    response = Response(msg)
    return response
