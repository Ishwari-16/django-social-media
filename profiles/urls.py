from . import views

from django.urls import path
from .views import (
    homepage,
    ProfileDetailView,
    FollowView,
    EditProfileView,
    EditProfileImageView,
    edit_name_username,
)

app_name = 'profiles'

urlpatterns = [
    path('', homepage, name='home'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('edit/', EditProfileView.as_view(), name='edit'),
    path('edit/', EditProfileView.as_view(), name='profile_edit'),
    path('edit/image/', EditProfileImageView.as_view(), name='edit_image'),
    path('edit-name-username/', edit_name_username, name='edit_name_username'),
]
