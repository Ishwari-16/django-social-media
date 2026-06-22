from . import views

from django.urls import path
from .views import (
    homepage,
    ProfileDetailView,
    FollowView,
    EditProfileView,
    EditProfileImageView,
    EditCoverPhotoView,
    edit_name_username,
    search,
)

app_name = 'profiles'

urlpatterns = [
    path('', homepage, name='home'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('edit/', EditProfileView.as_view(), name='edit'),
    path('edit/image/', EditProfileImageView.as_view(), name='edit_image'),
    path('edit/cover/', EditCoverPhotoView.as_view(), name='edit_cover'),
    path('edit-name-username/', edit_name_username, name='edit_name_username'),
    path('search/', search, name='search'),
    path(
    "<slug:username>/follow/",
    FollowView.as_view(),
    name="follow",
),
]
