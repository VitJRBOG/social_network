from django.apps import AppConfig
from threading import Thread


class NewsellerConfig(AppConfig):
    name = 'social_network.apps.newseller'

    def ready(self):
        Newseller().start()


class Newseller(Thread):

    def run(self):
        self.newseller()

    def newseller(self):
        import time
        from utils.logging import Logger
        
        while True:

            profiles = self.__fetch_all_profiles()

            if profiles['status'] != 200:
                Logger('warning').warning(profiles['response'])
                continue

            for profile_info in profiles['response']:
                text = ''

                feed_info = self.__fetch_feed(profile_info['id'])
                if feed_info['status'] != 200:
                    Logger('warning').warning(feed_info['response'])
                    continue

                for feed_post in feed_info['response']:
                    text += self.__parse_feedposts(feed_post)

                self.__send(profile_info['name'], text)

            time.sleep(86400)

    def __fetch_all_profiles(self):
        from ..accounts.views import GetProfileInfo
        profiles_resp = GetProfileInfo().select()

        return profiles_resp.data

    def __fetch_feed(self, profile_id):
        from ..feeds.views import GetFeed
        feed_posts_resp = GetFeed().select(profile_id, 0)

        return feed_posts_resp.data

    def __parse_feedposts(self, feed_post) -> str:
        text = f'\n\nПост от {feed_post["blog_name"]}\n{feed_post["title"]}\n{feed_post["text"]}'

        return text

    def __send(self, profile_name, top_posts):
        text = f'===\nТоп 5 постов для {profile_name}{top_posts}\n===\n'
        
        print(text)