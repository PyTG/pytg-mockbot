import logging

from telegram import Bot

from .MockRequest import MockRequest

class MockBot(Bot):
    def __init__(self):
        request = MockRequest()
        self.__add_validation_mock_responses(request)

        super(MockBot, self).__init__(token=None, base_url="mock.bot/", request = request)

    def _validate_token(self, token):
        return "mock:token" 

    def __add_validation_mock_responses(self, request):
        request.add_mock_response("GET", "getMe", {
            "id": 0,
            "is_bot": True,
            "first_name": "Mock Bot",
            "username": "MockBot",
            "can_join_groups": True,
            "can_read_all_group_messages": False,
            "supports_inline_queries": False
        })

        request.add_mock_response("GET", "getMyCommands", {})

        request.add_mock_response("POST", "deleteWebhook", {
            "{}": None
        })

        request.add_mock_response("POST", "getUpdates", {
            "{'timeout': 10, 'limit': 100}": []
        })