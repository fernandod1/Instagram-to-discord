import time

from src.config import Config
from src.constants import DELAY
from src.loop import Loop

if __name__ == "__main__":
    config = Config()
    users = [Loop(config, u) for u in config.users]

    while True:
        for user in users:
            user.run()
        time.sleep(DELAY)
