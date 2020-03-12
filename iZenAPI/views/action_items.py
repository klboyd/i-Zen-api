"""action_items for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import Progression, ActionItem
from .users import UsersSerializer
from .progressions import ProgressionsSerializer
from .action_item_status import ActionItemStatusesSerializer


class ActionItemsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for action_items

    Arguments:
        serializers
    """

    progression = ProgressionsSerializer()
    created_by = UsersSerializer()
    completed_by = UsersSerializer()
    status = ActionItemStatusesSerializer()

    class Meta:
        model = ActionItem
        url = serializers.HyperlinkedIdentityField(
            view_name="action_item", lookup_field="id"
        )
        fields = (
            "id",
            "url",
            "description",
            "due_at",
            "created_by",
            "created_at",
            "updated_at",
            "completed_by",
            "completed_at",
            "status",
            "progression",
        )
        depth = 1


class ActionItems(ViewSet):
    """note boards for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ActionItems instance
        """
        new_action_item = ActionItem()

        new_action_item.name = request.data["name"]
        new_action_item.description = request.data["description"]
        new_action_item.created_by_id = request.auth.user.id

        new_action_item.save()

        serializer = ActionItemsSerializer(
            new_action_item, context={"request": request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single action_item

        Returns:
            Response -- JSON serialized action_item instance
        """
        try:
            action_item = ActionItem.objects.get(pk=pk)
            serializer = ActionItemsSerializer(
                action_item, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a action_item

        Returns:
            Response -- Empty body with 204 status code
        """
        action_item = ActionItem.objects.get(pk=pk)

        action_item.name = request.data["name"]
        action_item.description = request.data["description"]
        action_item.created_at = action_item.created_at
        action_item.created_by_id = action_item.created_by_id

        action_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single action_item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            action_item = ActionItem.objects.get(pk=pk)
            action_item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ActionItems.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to action_items resource

        Returns:
            Response -- JSON serialized list of action_items
        """

        action_items = ActionItem.objects.all()

        serializer = ActionItemsSerializer(
            action_items, many=True, context={"request": request}
        )
        return Response(serializer.data)
