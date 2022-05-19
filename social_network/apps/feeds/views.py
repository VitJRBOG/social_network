from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from utils import logging
from ..accounts.views import GetFollowingInfo
from ..sources.views import GetBlog, GetBlogPost, GetBlogPostReadMark


class GetFeed(APIView):

    def get(self, request: Request):
        profile_id = request.query_params.get('profile_id')
        offset = request.query_params.get('offset')

        feed_resp = self.select(profile_id, offset)
        return feed_resp

    def select(self, profile_id, offset):
        try:
            followings_resp = GetFollowingInfo().select(profile_id)

            blog_ids = self.__parse_followings_for_blogs(followings_resp.data)

            blogposts_resp = GetBlogPost().select(blog_ids, offset)

            feed_posts = self.__compose_feed_posts(profile_id, blogposts_resp.data)

            return Response({
                    'status': 200,
                    'response': feed_posts
                })

        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка формирования ленты.'
                })

    def __parse_followings_for_blogs(self, data) -> str:
        followings_data = self.__parse_ordered_dicts(data['response'])
        blog_ids = ''
        for i, item in enumerate(followings_data):
            if i > 0:
                blog_ids += ','
            blog_ids += f'{item["blog_id"]}'
        return blog_ids

    def __compose_feed_posts(self, profile_id, blogposts_data):
        feed_posts = []

        blogposts = self.__parse_ordered_dicts(blogposts_data['response'])
        
        for blogpost in blogposts:
            blog_name = self.__fetch_blog_name(blogpost)
            readmark = self.__have_blogpost_read_mark(profile_id, blogpost)

            feed_post = {
                'blog_id': blogpost['blog_id'],
                'blog_name': blog_name,
                'blogpost_id': blogpost['id'],
                'is_read': readmark,
            }
            feed_posts.append(feed_post)

        return feed_posts


    def __fetch_blog_name(self, blogpost):
        blog_resp = GetBlog().select(blogpost['blog_id'])
        
        blog_info = self.__parse_ordered_dicts(blog_resp.data['response'])

        return blog_info[0]['name']

    def __have_blogpost_read_mark(self, profile_id, blogpost):
        read_mark_resp = GetBlogPostReadMark().select(profile_id, blogpost['id'])

        if read_mark_resp.data['status'] == 200:
            return True
        else:
            return False

    def __parse_ordered_dicts(self, ordered_dicts):
        s = json.dumps(ordered_dicts)
        json_dump = json.loads(s)

        return json_dump