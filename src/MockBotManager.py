import telegram, yaml

from telegram.ext import Updater

from modules.pytg.Manager import Manager
from modules.pytg.ModulesLoader import ModulesLoader

from .components.MockBot import MockBot
from .components.MockUpdater import MockUpdater

class MockBotManager(Manager):
    @staticmethod
    def initialize():
        MockBotManager.__instance = MockBotManager()

    @staticmethod
    def load():
        return MockBotManager.__instance

    def __init__(self):
        self.bot = MockBot()
        print(self.bot)
        self.updater = MockUpdater(mock_bot = self.bot)