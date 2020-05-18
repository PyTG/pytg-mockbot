import logging

from telegram import Bot

from .MockRequest import MockRequest

class MockBot(Bot):
    def __init__(self):
        super(MockBot, self).__init__(token=None, base_url="mock.bot/", request = MockRequest())

    def _validate_token(self, token):
        return "mock:token" 