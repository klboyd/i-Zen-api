"""retro_note_boards for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import RetroNoteBoard
from .users import UsersSerializer
from .retros import RetrosSerializer
from .note_boards import NoteBoardsSerializer


class RetroNoteBoardsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for retro_note_boards

    Arguments:
        serializers
    """

    retro = RetrosSerializer()
    note_board = NoteBoardsSerializer()

    class Meta:
        model = RetroNoteBoard
        url = serializers.HyperlinkedIdentityField(
            view_name="retro_note_board", lookup_field="id"
        )
        fields = ("id", "url", "retro", "note_board")
        depth = 2


class RetroNoteBoards(ViewSet):
    """note boards for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized RetroNoteBoards instance
        """
        new_retro_note_board = RetroNoteBoard()

        new_retro_note_board.retro_id = request.data["retro_id"]
        new_retro_note_board.note_board_id = request.data["note_board_id"]

        new_retro_note_board.save()

        serializer = RetroNoteBoardsSerializer(
            new_retro_note_board, context={"request": request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single retro_note_board

        Returns:
            Response -- JSON serialized retro_note_board instance
        """
        try:
            retro_note_board = RetroNoteBoard.objects.get(pk=pk)
            serializer = RetroNoteBoardsSerializer(
                retro_note_board, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single retro_note_board

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            retro_note_board = RetroNoteBoard.objects.get(pk=pk)
            retro_note_board.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RetroNoteBoards.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to retro_note_boards resource

        Returns:
            Response -- JSON serialized list of retro_note_boards
        """

        retro_note_boards = RetroNoteBoard.objects.all()

        serializer = RetroNoteBoardsSerializer(
            retro_note_boards, many=True, context={"request": request}
        )
        return Response(serializer.data)
