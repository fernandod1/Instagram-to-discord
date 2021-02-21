class User:
    def __init__(self, json):
        self.json = json

    @property
    def name(self) -> str:
        return self.json['username']

    @property
    def icon_url(self) -> str:
        return self.json['profile_pic_url']

    @property
    def link(self) -> str:
        return 'https://www.instagram.com/' + self.name

