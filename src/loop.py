from dhooks import Webhook
import dhooks

from src.config import Config
from src.instagram.post import Post
from src.instagram.scraper import Scraper
from src.instagram.user import User


class Loop:
    def __init__(self, config: Config, username):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
        self.last_image = 0

    def run(self):
        scraper = Scraper(self.username)
        post = scraper.get_last_post()
        user = scraper.get_user()

        if post.id == self.last_image:
            return

        embed = self.__create_embed(post, user)
        print(f'New post found\n{user.name} : {post.id}')
        self.webhook.send(embed=embed)
        self.last_image = post.id

    @staticmethod
    def __create_embed(post: Post, user: User) -> dhooks.Embed:
        embed = dhooks.Embed(description=post.caption)
        embed.color = 0xEC054C
        embed.set_image(post.image_url)
        embed.set_timestamp(time=post.timestamp)
        embed.set_footer(f'❤️ {post.likes} | 💬 {post.comments}')
        embed.set_author(name=user.name, icon_url=user.icon_url, url=user.link)

        return embed
