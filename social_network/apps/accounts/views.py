from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer


class AddProfile(APIView):

    def post(self, request: Request):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(request.data)
        else:
            return Response(serializer.errors)


class GetProfileInfo(APIView):

    def get(self, request: Request):
        id_ = request.query_params.get('id')

        queryset = Profile.objects.filter(id=id_)
        serializer = ProfileSerializer(instance=queryset, many=True)

        return Response(serializer.data)


class DeleteProfile(APIView):
    
    def post(self, request: Request):
        id_ = request.query_params.get('id')

        queryset = Profile.objects.filter(id=id_)
        count = queryset.count()

        queryset.delete()

        return Response(count)
