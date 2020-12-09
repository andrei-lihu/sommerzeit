#!/usr/bin/env python
import re
from datetime import date, timedelta, datetime

from html2text import HTML2Text
from skill_sdk import skill, Response
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import format_enumeration, get_jira_tasks, get_office365_account, get_mailbox

from summarizer.model_processors import Summarizer
from transformers import *


@skill.intent_handler("TEAM_24_UPDATE_ME")
def team_24_project_status_handler() -> Response:
    msg_emails = _("NO_EMAILS")
    mailbox = get_mailbox()
    query = mailbox.new_query().on_attribute('ReceivedDateTime').greater_equal(datetime(2020, 12, 5, 0, 0))
    titles = format_enumeration([message.subject + " " + _("FROM") + " " + message.sender.name for message in mailbox.get_messages(query=query)])
    if titles != "":
        msg_emails = _("EMAILS", titles=titles)

    msg_important_emails = ""
    important_messages = list(filter(lambda msg: msg.importance.name == 'High', mailbox.get_messages(query=query)))
    if len(important_messages) > 0:
        h = HTML2Text()
        h.ignore_links = True

        model = get_summarizer_model()
        content = ""
        for imp in important_messages:
            content = format_content(content, h, imp, model)

        msg_important_emails += _("IMPORTANT_EMAILS", content=content)

    done_tasks, done_tasks_count_msg, msg_done_tasks = get_done_tasks()
    if done_tasks_count_msg != _("NONE"):
        msg_done_tasks = _("DONE_TASKS_INTRO")
        msg_done_tasks += format_enumeration(done_tasks)
        msg_done_tasks += "."

    response = Response(msg_emails + " " + msg_important_emails + " " + msg_done_tasks)
    return response


def get_done_tasks():
    msg_done_tasks = _("NO_DONE_TASKS")
    today = date.today().strftime("%Y-%m-%d")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    done_q = 'project = {project} AND status changed during ({today}, {tomorrow}) to Done'. \
        format(project=config.get('jira', 'project'), today=today, tomorrow=tomorrow)
    done_tasks, done_tasks_count_msg = get_jira_tasks(done_q)
    return done_tasks, done_tasks_count_msg, msg_done_tasks


def format_content(content, h, imp, model):
    content += _("FROM") + " " + imp.sender.name + " " + _("WITH_SUBJECT") + " " + imp.subject + ": "
    body = h.handle(imp.body).replace('*', ''). \
        replace('|', '').replace('---', '').replace('[', ''). \
        replace(']', '').replace('#', '')
    body = re.sub(r'\n\s*\n', '\n\n', body)
    body = body.replace("\n", " ")
    summary = model(body)
    content += summary
    return content


def get_summarizer_model():
    model = config.get('ml', 'summarization_model')
    custom_config = AutoConfig.from_pretrained(model)
    custom_config.output_hidden_states = True
    custom_tokenizer = AutoTokenizer.from_pretrained(model)
    custom_model = AutoModel.from_pretrained(model, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
    return model
