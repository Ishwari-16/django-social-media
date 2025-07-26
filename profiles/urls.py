from django.urls import path, include

from . import views
from .views import ProfileDetailView, FollowView, EditProfileView, homepage

app_name="profiles"

urlpatterns = [
       path("", homepage, name="home"),
      path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
      path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
      path('edit/', views.edit_profile, name='edit'),

]