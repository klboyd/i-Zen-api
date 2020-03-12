"""note_boards for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import NoteBoard


class NoteBoardsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for note_boards

    Arguments:
        serializers
    """

    class Meta:
        model = NoteBoard
        url = serializers.HyperlinkedIdentityField(
            view_name="note_board", lookup_field="id"
        )
        fields = ("id", "url", "name", "board_type")
        depth = 2


class NoteBoards(ViewSet):
    """note boards for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized NoteBoard instance
        """
        new_note_board = NoteBoard()

        new_note_board.name = request.data["name"]
        new_note_board.board_type = request.data["board_type"]

        new_note_board.save()

        serializer = NoteBoardsSerializer(new_note_board, context={"request": request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single note_board

        Returns:
            Response -- JSON serialized note_board instance
        """
        try:
            note_board = NoteBoard.objects.get(pk=pk)
            serializer = NoteBoardsSerializer(note_board, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a note_board

        Returns:
            Response -- Empty body with 204 status code
        """
        note_board = NoteBoard.objects.get(pk=pk)

        note_board.name = request.data["name"]
        note_board.board_type = request.data["board_type"]
        note_board.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single note_board

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            note_board = NoteBoard.objects.get(pk=pk)
            note_board.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except NoteBoard.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to note_boards resource

        Returns:
            Response -- JSON serialized list of note_boards
        """

        note_boards = NoteBoard.objects.all()

        serializer = NoteBoardsSerializer(
            note_boards, many=True, context={"request": request}
        )
        return Response(serializer.data)
