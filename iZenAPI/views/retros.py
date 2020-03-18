"""retros for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import Retro
from .users import UsersSerializer
from .progressions import ProgressionsSerializer
from datetime import date


class RetrosSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for retros

    Arguments:
        serializers
    """

    created_by = UsersSerializer()
    progression = ProgressionsSerializer()

    class Meta:
        model = Retro
        url = serializers.HyperlinkedIdentityField(view_name="retro", lookup_field="id")
        fields = ("id", "url", "name", "created_by", "created_at", "progression")
        depth = 2


class Retros(ViewSet):
    """retros for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Retros instance
        """
        today = date.today().strftime("%A %b %d, %Y")
        progression_id = request.data["progression_id"]
        duplicate = Retro.objects.filter(progression__id=progression_id, name=today)

        if len(duplicate) == 0:
            new_retro = Retro()

            new_retro.name = today
            new_retro.progression_id = progression_id
            new_retro.created_by_id = request.auth.user.id

            new_retro.save()

            serializer = RetrosSerializer(new_retro, context={"request": request})

            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_302_FOUND)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single retro

        Returns:
            Response -- JSON serialized retro instance
        """
        try:
            retro = Retro.objects.get(pk=pk)
            serializer = RetrosSerializer(retro, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a retro

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            retro = Retro.objects.get(pk=pk)

            retro.name = request.data["name"]
            retro.progression_id = retro.progression_id
            retro.created_at = retro.created_at
            retro.created_by_id = retro.created_by_id

            retro.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Retros.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single retro

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            retro = Retro.objects.get(pk=pk)
            retro.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Retros.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to retros resource

        Returns:
            Response -- JSON serialized list of retros
        """

        progression_id = self.request.query_params.get("progression", None)

        if progression_id is not None:
            retros = Retro.objects.filter(progression__id=progression_id)
        else:
            retros = Retro.objects.all()

        serializer = RetrosSerializer(retros, many=True, context={"request": request})
        return Response(serializer.data)
