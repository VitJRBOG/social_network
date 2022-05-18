from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import logging
from .models import Following, Profile
from .serializers import ProfileSerializer, FollowingSerializer
from ..sources.models import Blog


class AddProfile(APIView):

    def post(self, request: Request):
        try:
            serializer = ProfileSerializer(data=request.data)

            if serializer.is_valid():
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
                    'response': 'Ошибка создания Профиля.'
                })


class GetProfileInfo(APIView):

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
        try:
            queryset = Following.objects.all()

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