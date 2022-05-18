from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import logging
from .models import Profile
from .serializers import ProfileSerializer


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

            if queryset.count == 0:
                return Response({
                        'status': 404,
                        'response': 'Записей с указанным "id" не найдено.'
                    })

        serializer = ProfileSerializer(instance=queryset, many=True)

        return Response(serializer.data)
            
        except Exception as e:
            logging.Logger('warning').warning(e)
            return Response({
                    'status': 500,
                    'response': 'Ошибка запроса выборки Профилей.'
                })


class DeleteProfile(APIView):
    
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

