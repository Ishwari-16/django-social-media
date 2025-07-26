from django.urls import path
from . import views
from .views import ProfileDetailView, FollowView, homepage

app_name = "profiles"

urlpatterns = [
    path("", homepage, name="home"),
    path("<str:username>/", ProfileDetailView.as_view(), name="detail"),
    path("<str:username>/follow/", FollowView.as_view(), name="follow"),
    path("edit/", views.edit_profile, name="edit"),
]
