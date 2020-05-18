import logging

from modules.mockbot.MockBotManager import MockBotManager

def initialize():
    logging.info("Initializing mockbot module...")

    MockBotManager.initialize()

def connect():
    pass

def load_manager():
    return MockBotManager.load() 

def main():
    # Start polling
    load_manager().updater.start_polling()
    logging.info("Mock bot polling.")

def depends_on():
    return ["config"]