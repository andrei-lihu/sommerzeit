#!/usr/bin/env python

from datetime import timedelta
from dateutil.parser import parse
from dateutil.tz import gettz
from skill_sdk import skill, Response
from skill_sdk.config import config
from skill_sdk.l10n import _

from impl.utils import get_office365_account, many_or_none_message, get_jira_account, get_jira_tasks, format_enumeration


@skill.intent_handler("TEAM_24_MY_DAY")
def team_24_my_day_handler() -> Response:
    """ TEAM_24_MY_DAY handler

    :return:
    """
    meetings, meetings_count_msg = get_meetings()

    tasks, tasks_count_msg = get_in_progress_tasks()

    msg = _("MY_DAY", nickname=config.get('jira', 'nickname'),
            meetings_count=meetings_count_msg, tasks_count=tasks_count_msg)

    if meetings_count_msg != _("NONE"):
        msg += " " + _("MY_MEETINGS_INTRO")
        msg += " ".join([m[1] + " " + _("AT") + " " + m[0] + "." for m in meetings])

    if tasks_count_msg != _("NONE"):
        msg += " " + _("MY_TASKS_INTRO")
        msg += format_enumeration(tasks)
        msg += "."

    response = Response(msg)
    return response


def get_in_progress_tasks():
    q = 'project = {project} AND assignee = currentUser() AND status IN ("In Progress") ORDER BY issuekey'. \
        format(project=config.get('jira', 'project'))
    return get_jira_tasks(q)


def get_meetings():
    office365_account = get_office365_account()
    schedule = office365_account.schedule()
    calendar = schedule.get_default_calendar()
    meetings = get_day_meetings(calendar)
    meetings_count_msg = many_or_none_message(meetings)
    return meetings, meetings_count_msg


def get_day_meetings(calendar):
    berlin = gettz('Europe/Berlin')
    tz_infos = {'CET': berlin, 'CEST': berlin}
    day = parse(config.get('office365', 'day'), dayfirst=True, tzinfos=tz_infos)
    next_day = day + timedelta(days=1)
    q = calendar.new_query('start').greater_equal(day)
    q.chain('and').on_attribute('end').less(next_day)
    return [("{:d}:{:02d}".format(m.start.hour, m.start.minute), m.subject) for m in
            calendar.get_events(query=q, include_recurring=True)]
