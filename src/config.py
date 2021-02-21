from typing import List

import yaml


class Config:
    def __init__(self):
        with open("../config.yml", "r") as stream:
            self.data = yaml.safe_load(stream)

    @property
    def webhook_url(self) -> str:
        return self.data['webhook_url']

    @property
    def users(self) -> List[str]:
        return self.data['users']
