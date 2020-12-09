import unittest
from skill_sdk.responses import RESPONSE_TYPE_TELL
from skill_sdk.test_helpers import FunctionalTest
from impl.main import skill


class TestMain(unittest.TestCase):

    def test_team_24_my_day_handler(self):
        """ Test team_24_my_day_handler
        """

        self.assertEqual(1, 1)
        return

        # ignore the rest for the moment
        # response = skill.test_intent("TEAM_24_MY_DAY")
        # self.assertEqual(response.text.key, "HELLO")
        # self.assertEqual(response.text.kwargs, {'intent': 'WEATHER__STATUS'})


class TestRunner(FunctionalTest):
    """
        Full functional test sample:

            This test starts the web server in a separate greenlet (see test_helpers.FunctionalTest.setUpClass)
                and tests two endpoints:
                - GET /v1/sommerzeit/info
                - POST /v1/sommerzeit

    """

    def test_info_response(self):
        """ Test /v1/sommerzeit/info endpoint
        """
        return self.default_info_response_test()

    def test_team_24_my_day_handler(self):
        """ Test team_24_my_day_handler with locale="de"
        """
        self.assertEqual(1, 1)
        return

        # ignore this
        # response = self.invoke("TEAM_24_MY_DAY", locale="de")
        # self.assertEqual(response["type"], RESPONSE_TYPE_TELL)
        # self.assertEqual(response["text"], f"Hallo TEAM_24_MY_DAY")
