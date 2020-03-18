"""action_item_statuses for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import ActionItemStatus


class ActionItemStatusesSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for action_item_statuses

    Arguments:
        serializers
    """

    class Meta:
        model = ActionItemStatus
        url = serializers.HyperlinkedIdentityField(
            view_name="action_item_status", lookup_field="id"
        )
        fields = (
            "id",
            "url",
            "name",
        )
        # depth = 0


class ActionItemStatuses(ViewSet):
    """note boards for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ActionItemStatuses instance
        """
        new_action_item_status = ActionItemStatus()

        new_action_item_status.name = request.data["name"]

        new_action_item_status.save()

        serializer = ActionItemStatusesSerializer(
            new_action_item_status, context={"request": request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single action_item_status

        Returns:
            Response -- JSON serialized action_item_status instance
        """
        try:
            action_item_status = ActionItemStatus.objects.get(pk=pk)
            serializer = ActionItemStatusesSerializer(
                action_item_status, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a action_item_status

        Returns:
            Response -- Empty body with 204 status code
        """
        action_item_status = ActionItemStatus.objects.get(pk=pk)

        action_item_status.name = request.data["name"]
        action_item_status.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single action_item_status

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            action_item_status = ActionItemStatus.objects.get(pk=pk)
            action_item_status.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ActionItemStatuses.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to action_item_statuses resource

        Returns:
            Response -- JSON serialized list of action_item_statuses
        """

        action_item_statuses = ActionItemStatus.objects.all()

        serializer = ActionItemStatusesSerializer(
            action_item_statuses, many=True, context={"request": request}
        )
        return Response(serializer.data)
