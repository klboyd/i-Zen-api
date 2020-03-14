import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register_user(request):
    """Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    """

    req_body = json.loads(request.body.decode())

    email = req_body.get("email")
    first_name = req_body.get("first_name") or ""
    last_name = req_body.get("last_name") or ""

    new_user = User.objects.create_user(
        username=req_body["username"],
        email=email,
        password=req_body["password"],
        first_name=first_name,
        last_name=last_name,
        is_active=True,
    )

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type="application/json")

