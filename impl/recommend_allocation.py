from collections import defaultdict
from math import ceil

from skill_sdk import skill, Response
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import get_jira_account, get_jira_tasks, get_project_users_without_pm, format_enumeration, get_backlog


@skill.intent_handler("TEAM_24_RECOMMEND_ALLOCATION")
def team_24_recommend_allocation_handler() -> Response:
    """ TEAM_24_RECOMMEND_ALLOCATION handler

    :return:
    """
    allocation_table = list()
    jira_account = get_jira_account()
    users = get_project_users_without_pm()

    q = "project = {project} AND assignee = '{user}' AND status IN ('To Do', 'In Progress') ORDER BY issuekey"
    total = 0
    for user in users:
        q_user = q.format(project=config.get('jira', 'project'), user=user)
        tasks, tasks_count_msg = get_jira_tasks(q_user, jira_account)
        allocation_table.append((user, len(tasks)))
        total += len(tasks)

    tasks, tasks_count_msg = get_backlog(jira_account)
    if tasks_count_msg == _("NONE"):
        return _("NO_BACKLOG")

    summary = allocate_backlog(tasks, allocation_table, total, users)
    msg = _("RECOMMENDER_INTRO")
    for usr, ts in summary.items():
        msg += _("RECOMMENDER_SG", tasks=format_enumeration(ts)) if len(ts) == 1 else _("RECOMMENDER_PL", tasks=format_enumeration(ts)) + _("TO") + " " + usr + ". "

    response = Response(msg)
    return response


def allocate_backlog(tasks, allocation_table, total, users):
    backlog = len(tasks)
    allocation_table.sort(key=lambda x: x[1])
    avg = ceil(total / len(users))
    summary = defaultdict(list)
    i, j = 0, 0
    while backlog > 0:
        temp = allocation_table[i]
        if temp[1] <= avg:
            allocation_table[i] = (temp[0], temp[1] + 1)
            summary[allocation_table[i][0]].append(tasks[j])
            total += 1
            j += 1
            backlog -= 1
        if i >= len(users) - 1:
            i = 0
            avg = ceil(total / len(users))
        else:
            i += 1
    return summary
