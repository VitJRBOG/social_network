from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import logging
from .models import Blog, BlogPost, BlogPostReadMark
from .serializers import BlogSerializer, BlogPostSerializer, BlogPostReadMarkSerializer
from ..accounts.models import Profile


class AddBlog(APIView):
    def post(self, request: Request):
        try:
            serializer = BlogSerializer(data=request.data)

            if serializer.is_valid():

                profile_id = serializer.validated_data.get('profile_id')  # type: ignore

                if not Profile.objects.filter(id=profile_id).exists():
                    return Response({
                            'status': 404,
                            'response': 'Профиль с указанным "profile_id" не найден.'
                        })

                serializer.save()

                return Response({
                        'status': 200,
                        'response': serializer.data
                    })
            else:
                return Response({
                        'status': 400,
                        'response': serializer.errors
                    })
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка создания Блога.'
                })


class GetBlog(APIView):
    def get(self, request: Request):
        id_ = request.query_params.get('id')
        
        response = self.select(id_)
        return response
            

    def select(self, id_) -> Response:
        try:
            if id_ is None:
                return Response({
                    'status': 400,
                    'response': {
                        'id':
                            [
                                'Обязательное поле.'
                            ]
                        }
                    })

            queryset = Blog.objects.filter(id=id_)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанным "id" не найдено.'
                    })

            serializer = BlogSerializer(instance=queryset, many=True)

            return Response({
                    'status': 200,
                    'response': serializer.data
                })
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка запроса выборки Блогов.'
                })


class DeleteBlog(APIView):
    def post(self, request: Request):
        try:
            id_ = request.POST.get('id')  # type: ignore

            if id_ is None:
                return Response({
                    'status': 400,
                    'response': {
                        'id':
                            [
                                'Обязательное поле.'
                            ]
                        }
                    })

            queryset = Blog.objects.filter(id=id_)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанным "id" не найдено.'
                    })

            queryset.delete()

            return Response({
                    'status': 200
                })

        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка удаления Блога.'
                })


class AddBlogPost(APIView):
    def post(self, request: Request):
        try:
            serializer = BlogPostSerializer(data=request.data)

            if serializer.is_valid():

                blog_id = serializer.validated_data.get('blog_id')  # type: ignore

                if not Blog.objects.filter(id=blog_id).exists():
                    return Response({
                            'status': 404,
                            'response': 'Блог с указанным "blog_id" не найден.'
                        })

                serializer.save()

                return Response({
                        'status': 200,
                        'response': request.data
                    })
            else:
                return Response({
                        'status': 400,
                        'response': serializer.errors
                    })
        
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка создания поста блога.'
                })


class GetBlogPost(APIView):
    def get(self, request: Request):

        blog_ids = request.query_params.get('blog_ids')
        
        offset = request.query_params.get('offset')

        response = self.select(blog_ids, offset)
        return response

    def select(self, blog_ids, offset) -> Response:
        try:
            condition = self.__compose_condition(blog_ids)

            if offset is None:
                offset = 0
            else:
                offset = int(offset)

            queryset = BlogPost.objects.extra(where=[condition]).order_by('date')[offset:offset+10]

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Ни одной записи не найдено.'
                    })

            serializer = BlogPostSerializer(instance=queryset, many=True)

            return Response({
                    'status': 200,
                    'response': serializer.data
                })

        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка получения постов блога.'
                })

    def __compose_condition(self, blog_ids) -> str:
        condition = ''
        ids = blog_ids.split(',')
        for i, item in enumerate(ids):
            if i > 0:
                condition += ' or '
            condition += f'blog_id={item}'
        
        return condition


class DeleteBlogPost(APIView):
    def post(self, request: Request):
        try:
            id_ = request.POST.get('id')  # type: ignore

            if id_ is None:
                return Response({
                    'status': 400,
                    'response': {
                        'id':
                            [
                                'Обязательное поле.'
                            ]
                        }
                    })

            queryset = BlogPost.objects.filter(id=id_)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанным "id" не найдено.'
                    })

            queryset.delete()

            return Response({
                    'status': 200
                })

        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка удаления поста блога.'
                })


class AddBlogPostReadMark(APIView):
    def post(self, request: Request):
        try:
            serializer = BlogPostReadMarkSerializer(data=request.data)

            if serializer.is_valid():

                profile_id = serializer.validated_data.get('profile_id')  # type: ignore

                if not Profile.objects.filter(id=profile_id).exists():
                    return Response({
                            'status': 404,
                            'response': 'Профиль с указанным "profile_id" не найден.'
                        })

                blogpost_id = serializer.validated_data.get('blogpost_id')  # type: ignore

                if not BlogPost.objects.filter(id=blogpost_id).exists():
                    return Response({
                            'status': 404,
                            'response': 'Пост с указанным "blogpost_id" не найден.'
                        })

                serializer.save()

                return Response({
                        'status': 200,
                        'response': serializer.data
                    })
            else:
                return Response({
                        'status': 400,
                        'response': serializer.errors
                    })
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка создания метки "Прочитано".'
                })


class GetBlogPostReadMark(APIView):
    def get(self, request: Request):
        profile_id = request.query_params.get('profile_id')

        blogpost_id = request.query_params.get('blogpost_id')

        response = self.select(profile_id, blogpost_id)            
        return response

    def select(self, profile_id, blogpost_id) -> Response:
        try:
            if profile_id is None:
                return Response({
                    'status': 400,
                    'response': {
                        'profile_id':
                            [
                                'Обязательное поле.'
                            ]
                        }
                    })

            if not Profile.objects.filter(id=profile_id).exists():
                return Response({
                        'status': 404,
                        'response': 'Профиль с указанным "profile_id" не найден.'
                    })
            
            if blogpost_id is None:
                return Response({
                    'status': 400,
                    'response': {
                        'blogpost_id':
                            [
                                'Обязательное поле.'
                            ]
                        }
                    })

            if not BlogPost.objects.filter(id=blogpost_id).exists():
                return Response({
                        'status': 404,
                        'response': 'Пост с указанным "blogpost_id" не найден.'
                    })

            queryset = BlogPostReadMark.objects.filter(profile_id=profile_id).filter(blogpost_id=blogpost_id)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанными "profile_id" и "blogpost_id" не найдено.'
                    })

            serializer = BlogPostReadMarkSerializer(instance=queryset, many=True)

            return Response({
                    'status': 200,
                    'response': serializer.data
                })
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка запроса выборки меток "Прочитано".'
                })


class DeleteBlogPostReadMark(APIView):
    def post(self, request: Request):
        try:
            id_ = request.POST.get('id')  # type: ignore

            if id_ is None:
                return Response({
                    'status': 400,
                    'response': {
                        'id':
                            [
                                'Обязательное поле.'
                            ]
                        }
                    })

            queryset = BlogPostReadMark.objects.filter(id=id_)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанным "id" не найдено.'
                    })

            queryset.delete()

            return Response({
                    'status': 200
                })

        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка удаления метки "Прочитано".'
                })
