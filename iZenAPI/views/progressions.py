"""progressions for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import Progression
from .users import UsersSerializer


class ProgressionsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for progressions

    Arguments:
        serializers
    """

    created_by = UsersSerializer()

    class Meta:
        model = Progression
        url = serializers.HyperlinkedIdentityField(
            view_name="progression", lookup_field="id"
        )
        fields = ("id", "url", "name", "description", "created_at", "created_by")
        depth = 0


class Progressions(ViewSet):
    """note boards for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Progressions instance
        """
        new_progression = Progression()

        new_progression.name = request.data["name"]
        new_progression.description = request.data["description"]
        new_progression.created_by_id = request.auth.user.id

        new_progression.save()

        serializer = ProgressionsSerializer(
            new_progression, context={"request": request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single progression

        Returns:
            Response -- JSON serialized progression instance
        """
        try:
            progression = Progression.objects.get(pk=pk)
            serializer = ProgressionsSerializer(
                progression, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a progression

        Returns:
            Response -- Empty body with 204 status code
        """
        progression = Progression.objects.get(pk=pk)

        progression.name = request.data["name"]
        progression.description = request.data["description"]
        progression.created_at = progression.created_at
        progression.created_by_id = progression.created_by_id

        progression.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single progression

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            progression = Progression.objects.get(pk=pk)
            progression.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Progressions.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to progressions resource

        Returns:
            Response -- JSON serialized list of progressions
        """

        user_id = request.auth.user.id

        progressions = Progression.objects.filter(created_by__id=user_id)

        serializer = ProgressionsSerializer(
            progressions, many=True, context={"request": request}
        )
        return Response(serializer.data)
