from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer


class AddProfile(APIView):

    def post(self, request: Request):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(request.data)
        else:
            return Response(serializer.errors)


