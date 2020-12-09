#!/usr/bin/env python

""" This is a dummy implementation of the intents:
    "TEAM_24_MY_DAY"
    "TEAM_24_UPDATE_ME"
    "TEAM_24_NEW_TASK"
    "TEAM_24_ASSIGN_TASK"
    "TEAM_24_PROJECT_STATUS"
    "TEAM_24_RECOMMEND_ALLOCATION"
    "TEAM_24_CALL"
    "TEAM_24_SCHEDULE_MEETING"
    
"""

from skill_sdk import skill, Response, ask, tell
from skill_sdk.l10n import _


@skill.intent_handler("TEAM_24_SCHEDULE_MEETING")
def team_24_schedule_meeting_handler(usernames: str, time: str) -> Response:
    """ TEAM_24_SCHEDULE_MEETING handler
        
    :param usernames: str
    :param time: str
    :return:
    """
    response = Response(_("NOT_IMPLEMENTED", intent="TEAM_24_SCHEDULE_MEETING"))
    return response


if __name__ == '__main__':  # pragma: no cover
    skill.run()
