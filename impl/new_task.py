from skill_sdk import skill, Response, ask, tell
from skill_sdk.l10n import _
from skill_sdk.config import config

from impl.utils import get_jira_account, get_current_project


@skill.intent_handler("TEAM_24_NEW_TASK")
def team_24_new_task_handler(taskname: str) -> Response:
    """ TEAM_24_NEW_TASK handler

    :param taskname: str
    :return:
    """

    jira_account = get_jira_account()
    my_project = get_current_project(jira_account)

    issue_dict = {
        'project': {'key': '{project}'.format(project=my_project['key'])},
        'issuetype': {'name': 'Story'},
        'summary': '{taskname}'.format(taskname=taskname)
    }
    jira_account.issue_create_or_update(fields=issue_dict)

    response = Response(_("NEW_TASK", taskname=taskname))
    return response
