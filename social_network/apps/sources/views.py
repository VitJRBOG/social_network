from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import logging
from .models import Blog, BlogPost
from .serializers import BlogSerializer, BlogPostSerializer
from ..accounts.models import Profile


class AddBlog(APIView):
    def post(self, request: Request):
        try:
            serializer = BlogSerializer(data=request.data)

            if serializer.is_valid():

                profile_id = request.query_params.get('profile_id')

                if not Profile.objects.filter(id=profile_id).exists():
                    return Response({
                            'status': 404,
                            'response': 'Профиль с указанным "profile_id" не найден.'
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
                    'response': 'Ошибка создания Блога.'
                })


class GetBlog(APIView):
    def get(self, request: Request):
        try:
            id_ = request.query_params.get('id')

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
            id_ = request.query_params.get('id')

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

                blog_id = request.query_params.get('blog_id')

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
        try:
            queryset = BlogPost.objects.all()

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


class DeleteBlogPost(APIView):
    def post(self, request: Request):
        try:
            id_ = request.query_params.get('id')

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
