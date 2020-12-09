import os

from O365 import Account, FileSystemTokenBackend
from atlassian import Jira
from skill_sdk.config import config
from skill_sdk.l10n import _

import configparser

from impl.fuzzy_words import similarity

config_secrets = configparser.ConfigParser()
config_secrets.read('creds.conf')
TOKEN_DIR = config_secrets.get('office365', 'token_dir')


def ensure_token_dir():
    if not os.path.exists(TOKEN_DIR):
        os.makedirs(TOKEN_DIR)


def get_office365_account():
    credentials = (config_secrets.get('office365', 'client_id'), config_secrets.get('office365', 'client_secret'))

    ensure_token_dir()

    token_backend = FileSystemTokenBackend(token_path=TOKEN_DIR, token_filename='token.txt')
    account = Account(credentials, main_resource=config_secrets.get('office365', 'username'),
                      auth_flow_type='credentials', tenant_id=config_secrets.get('office365', 'tenant_id'),
                      token_backend=token_backend)
    account.authenticate()
    return account


def get_jira_account():
    jira = Jira(
        url=config_secrets.get('jira', 'url'),
        username=config_secrets.get('jira', 'username'),
        password=config_secrets.get('jira', 'secret_token'))
    return jira


def get_jira_tasks(q, account=None):
    jira_account = account
    if jira_account is None:
        jira_account = get_jira_account()

    if jira_account is None:
        return [], _("NONE")

    q_res = jira_account.jql(q)
    tasks = [t['fields']['summary'] for t in q_res['issues']]
    tasks_count_msg = many_or_none_message(tasks)
    return tasks, tasks_count_msg


def many_or_none_message(entities):
    entities_count_msg = str(len(entities))
    if entities_count_msg == "0":
        entities_count_msg = _("NONE")
    return entities_count_msg


def get_project_users():
    return [u.strip() for u in config.get('jira', 'team').split(',')]


def get_project_users_without_pm():
    users = get_project_users()
    users.remove(config.get('jira', 'fullname'))
    return users


def format_enumeration(entities):
    entity_final_str = (" " + _("AND") + " ").join(
        [", ".join(entities[:-1]), entities[-1]] if len(entities) > 2 else entities)
    return entity_final_str


def get_mailbox():
    office365_account = get_office365_account()
    mailbox = office365_account.mailbox(resource=config_secrets.get('office365', 'username'))
    return mailbox


def get_current_project(jira_account):
    my_project = next((prj for prj in jira_account.get_all_projects() if prj['name'] == config.get('jira', 'project')),
                      None)
    return my_project


def get_backlog(jira_account):
    backlog_tasks_q = 'project = {project} AND sprint IS EMPTY OR sprint IN closedSprints()  AND sprint NOT IN (' \
                      'openSprints(), futureSprints()) AND status != Done '.format(project=config.get('jira',
                                                                                                      'project'))
    return get_jira_tasks(backlog_tasks_q, jira_account)


def clarify_user(username):
    team_users = [u.strip() for u in config.get('jira', 'team').split(',')]
    chosen_user = choose_entity(team_users, username)
    return chosen_user


def choose_entity(entities, entity):
    similarities = [similarity(entity, u) for u in entities]
    sim_index = similarities.index(min(similarities))
    if sim_index >= 0:
        return entities[sim_index]
    return None


def choose_entity_from_tuples(entities, entity):
    similarities = [similarity(entity, u[1]) for u in entities]
    sim_index = similarities.index(min(similarities))
    if sim_index >= 0:
        return entities[sim_index]
    return None


def get_jira_tasks_with_due_dates(q, account=None):
    q_res = account.jql(q)
    tasks = [(t['fields']['summary'], t['fields']['duedate']) for t in q_res['issues']]
    return tasks
