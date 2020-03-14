import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

# from django.core.exceptions import ValidationError


@csrf_exempt
def register_user(request):
    """Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    """

    req_body = json.loads(request.body.decode())
    # if User.objects.filter(username=req_body.get("username")).exists():
    #     raise ValidationError("This username already exists.")

    username = req_body.get("username")
    email = req_body.get("email")
    first_name = req_body.get("first_name") or ""
    last_name = req_body.get("last_name") or ""

    is_already_exists = User.objects.filter(username=username).exists()
    if not is_already_exists:
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=req_body["password"],
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )

        token = Token.objects.create(user=new_user)

        response = Response(
            {"token": token.key},
            content_type="application/json",
            status=status.HTTP_201_CREATED,
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response

    else:
        response = Response(
            {"error": "Username already exists."},
            content_type="application/json",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response

