from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import logging
from .models import Following, Profile
from .serializers import ProfileSerializer, FollowingSerializer
from ..sources.models import Blog
from ..sources.views import AddBlog


class UserRegistration(APIView):
    def post(self, request: Request):

        profile_info = {
            'name': request.POST.get('name'),  # type: ignore
            'login': request.POST.get('login'),  # type: ignore
            'password_hash': request.POST.get('password_hash'),  # type: ignore
        }

        add_profile_resp = AddProfile().insert(profile_info)

        if add_profile_resp.data['status'] != 200:
            return add_profile_resp

        blog_info = {
            'name': profile_info['name'],
            'profile_id': add_profile_resp.data['response']['id'],
        }

        add_blog_resp = AddBlog().insert(blog_info)

        if add_blog_resp.data['status'] != 200:
            return add_blog_resp

        user_info = {
            'login': profile_info['login'],
            'password_hash': profile_info['password_hash'],
            'profile_id': blog_info['profile_id'],
            'profile_name': profile_info['name'],
            'blog_id': add_blog_resp.data['response']['id'],
            'blog_name': blog_info['name'],
        }
        
        return Response({
            'status': 200,
            'response': user_info,
        })


class AddProfile(APIView):

    def post(self, request: Request):
        response = self.insert(request.data)
        return response

    def insert(self, data):
        try:
            serializer = ProfileSerializer(data=data)

            if serializer.is_valid():
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
                    'response': 'Ошибка создания Профиля.'
                })


class GetProfileInfo(APIView):

    def get(self, request: Request):
        id_ = request.query_params.get('id')

        response = self.select(id_)
        return response

    def select(self, id_):
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

            queryset = Profile.objects.filter(id=id_)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанным "id" не найдено.'
                    })

            serializer = ProfileSerializer(instance=queryset, many=True)

            return Response({
                    'status': 200,
                    'response': serializer.data
                })
            
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка запроса выборки Профилей.'
                })


class DeleteProfile(APIView):
    
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

            queryset = Profile.objects.filter(id=id_)

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
                    'response': 'Ошибка удаления Профиля.'
                })


class AddFollowing(APIView):
    def post(self, request: Request):
        try:
            serializer = FollowingSerializer(data=request.data)

            if serializer.is_valid():
                profile_id = serializer.validated_data.get('profile_id')  # type: ignore

                if not Profile.objects.filter(id=profile_id).exists():
                    return Response({
                            'status': 404,
                            'response': 'Профиль с указанным "profile_id" не найден.'
                        })

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
                    'response': 'Ошибка создания Подписки.'
                })


class GetFollowingInfo(APIView):
    def get(self, request: Request):
        profile_id = request.query_params.get('profile_id')

        response = self.select(profile_id)
        return response

    def select(self, profile_id) -> Response:
        try:
            
            if not Profile.objects.filter(id=profile_id).exists():
                return Response({
                        'status': 404,
                        'response': 'Профиль с указанным "profile_id" не найден.'
                    })

            queryset = Following.objects.filter(profile_id=profile_id)

            if queryset.count() == 0:
                return Response({
                        'status': 404,
                        'response': 'Ни одной записи не найдено.'
                    })

            serializer = FollowingSerializer(instance=queryset, many=True)

            return Response({
                    'status': 200,
                    'response': serializer.data
                })

        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка получения подписок.'
                })


class DeleteFollowing(APIView):
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

            queryset = Following.objects.filter(id=id_)

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
                    'response': 'Ошибка удаления Подписки.'
                })