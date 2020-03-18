"""notes for iZenAPI"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from iZenAPI.models import Note
from .users import UsersSerializer
from .retro_note_boards import RetroNoteBoardsSerializer


class NotesSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for notes

    Arguments:
        serializers
    """

    created_by = UsersSerializer()
    retro_note_board = RetroNoteBoardsSerializer()

    class Meta:
        model = Note
        url = serializers.HyperlinkedIdentityField(view_name="note", lookup_field="id")
        fields = (
            "id",
            "url",
            "description",
            "created_by",
            "created_at",
            "updated_at",
            "retro_note_board",
        )
        # depth = 0


class Notes(ViewSet):
    """note boards for iZenAPI"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Notes instance
        """
        new_note = Note()

        new_note.description = request.data["description"]
        new_note.retro_note_board_id = request.data["retro_note_board_id"]
        new_note.created_by_id = request.auth.user.id

        new_note.save()

        serializer = NotesSerializer(new_note, context={"request": request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single note

        Returns:
            Response -- JSON serialized note instance
        """
        try:
            note = Note.objects.get(pk=pk)
            serializer = NotesSerializer(note, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a note

        Returns:
            Response -- Empty body with 204 status code
        """
        note = Note.objects.get(pk=pk)

        note.description = request.data["description"]
        note.retro_note_board_id = note.retro_note_board_id
        note.created_at = note.created_at
        note.created_by_id = note.created_by_id

        note.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single note

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            note = Note.objects.get(pk=pk)
            note.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Notes.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to notes resource

        Returns:
            Response -- JSON serialized list of notes
        """
        retro_id = self.request.query_params.get("retro", None)

        notes = Note.objects.filter(retro_note_board__retro__id=retro_id).order_by(
            "-retro_note_board__note_board__board_type"
        )

        serializer = NotesSerializer(notes, many=True, context={"request": request})
        return Response(serializer.data)
