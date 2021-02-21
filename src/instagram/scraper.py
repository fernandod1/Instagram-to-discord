import requests

from src.constants import INSTAGRAM_URL
from src.instagram.post import Post
from src.instagram.user import User


class Scraper:
    def __init__(self, username: str):
        res = self.__get_instagram_feed(username)
        self.json = res.json()['graphql']

    @staticmethod
    def __get_instagram_feed(username: str) -> requests.Response:
        headers = {
            'Host': 'www.instagram.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                          'Safari/537.11 '
        }

        return requests.get(INSTAGRAM_URL + username + '/feed/?__a=1', headers=headers)

    def get_last_post(self) -> Post:
        return self.get_post(0)

    def get_post(self, num: int) -> Post:
        post = self.json['user']['edge_owner_to_timeline_media']['edges'][num]['node']
        return Post(post)

    def get_user(self) -> User:
        return User(self.json['user'])


