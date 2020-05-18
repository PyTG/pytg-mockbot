import logging

from telegram.ext import Updater

class MockUpdater(Updater):
    def __init__(self, mock_bot):
        super(MockUpdater, self).__init__(bot = mock_bot)