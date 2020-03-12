import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse


@csrf_exempt
def login_user(request):
    """Handles the authentication of a user
    Method arguments:
      request -- The full HTTP request object
    """

    req_body = json.loads(request.body.decode())

    if request.method == "POST":

        username = req_body["username"]
        password = req_body["password"]
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type="application/json")
        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type="application/json")
