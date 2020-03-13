"""iZen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path
from iZenAPI.models import *
from iZenAPI.views import (
    login_user,
    register_user,
    Users,
    NoteBoards,
    ActionItemStatuses,
    Progressions,
    ActionItems,
    Retros,
    RetroNoteBoards,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"users", Users, "user")
router.register(r"noteboards", NoteBoards, "noteboard")
router.register(r"actionitemstatus", ActionItemStatuses, "actionitemstatus")
router.register(r"progressions", Progressions, "progression")
router.register(r"actionitems", ActionItems, "actionitem")
router.register(r"retros", Retros, "retro")
router.register(r"retronoteboards", RetroNoteBoards, "retronoteboard")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth/", obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
