from skill_sdk import skill, Response, ask, tell, config
from skill_sdk.l10n import _
from skill_sdk.config import config

from impl.utils import get_jira_account, get_jira_tasks, many_or_none_message, clarify_user, choose_entity_from_tuples


@skill.intent_handler("TEAM_24_ASSIGN_TASK")
def team_24_assign_task_handler(username: str, taskname: str) -> Response:
    """ TEAM_24_ASSIGN_TASK handler

    :param username: str
    :param taskname: str
    :return:
    """

    chosen_user = clarify_user(username)

    jira_account = get_jira_account()
    tasks, tasks_count_msg = get_all_jira_tasks_with_keys(jira_account)
    if tasks_count_msg == _("NONE"):
        return Response(_("EMPTY_PROJECT", intent="TEAM_24_NEW_TASK"))

    chosen_task = choose_entity_from_tuples(tasks, taskname)

    if chosen_task is None or chosen_user is None:
        return Response(_("CANNOT_UNDERSTAND", intent="TEAM_24_NEW_TASK"))

    assignable_users = jira_account.get_assignable_users_for_issue(chosen_task[0])
    user_with_account_id = next(filter(lambda user: user['displayName'] == chosen_user, assignable_users), None)

    if user_with_account_id is None:
        return Response(_("CANNOT_UNDERSTAND", intent="TEAM_24_NEW_TASK"))

    account_id_user = user_with_account_id['accountId']
    jira_account.issue_update(chosen_task[0], fields={"assignee": {"accountId": account_id_user}})

    response = Response(_("ASSIGN_TASK", intent="TEAM_24_NEW_TASK", username=chosen_user))
    return response


def get_all_jira_tasks_with_keys(jira_account):
    q = "project = {project} order by created DESC".format(project=config.get('jira', 'project'))
    q_res = jira_account.jql(q)
    tasks = [(t['key'], t['fields']['summary']) for t in q_res['issues']]
    tasks_count_msg = many_or_none_message(tasks)
    return tasks, tasks_count_msg
