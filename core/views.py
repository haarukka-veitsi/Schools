from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from core.exeptions import NotFoundException, InternalErrorException
from core.models import School
from core.serializers import SchoolSerializer


class BaseViewSet(ViewSet):
    model = None
    serializer_class = None
    list_name = "list"
    object_name = "object"

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFoundException()

    def list(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {self.list_name: serializer.data}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response(
            {self.object_name: serializer.data}, status=status.HTTP_200_OK
        )

    def create(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data[self.object_name]
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {self.object_name: serializer.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            raise InternalErrorException(str(e))

    def partial_update(self, request, pk=None):
        obj = self.get_object(pk)
        try:
            serializer = self.serializer_class(
                obj, data=request.data[self.object_name], partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {self.object_name: serializer.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            raise InternalErrorException(str(e))

    def destroy(self, request, pk=None):
        obj = self.get_object(pk)
        try:
            obj.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            raise InternalErrorException(str(e))


class SchoolViewSet(BaseViewSet):
    model = School
    serializer_class = SchoolSerializer
    list_name = "list"
    object_name = "school"
