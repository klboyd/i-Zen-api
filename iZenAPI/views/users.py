from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for users
    Arguments:
        serializers
    """

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(view_name="user", lookup_field="id")
        fields = ("id", "url", "username", "last_name", "first_name", "email")


class Users(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UsersSerializer(user, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests multiple users
        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()

        # user = self.request.query_params.get('user', None)

        # if user is not None:
        #     users = users.filter(id=user)

        serializer = UsersSerializer(users, many=True, context={"request": request})

        return Response(serializer.data)
