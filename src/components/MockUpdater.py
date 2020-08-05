import logging

from telegram.ext import Updater

class MockUpdater(Updater):
    def __init__(self, mock_bot):
        super(MockUpdater, self).__init__(bot = mock_bot)

    # TODO: Check if disabling the updating thread causes issues to the workflow
    def _init_thread(self, target, name, *args, **kwargs):
        return