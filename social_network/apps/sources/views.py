from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import logging
from ..accounts.models import Profile
from .serializers import BlogSerializer


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
