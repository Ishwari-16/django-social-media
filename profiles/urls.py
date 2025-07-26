from django.urls import path
from .views import ProfileDetailView, FollowView, EditProfileView, homepage
from . import views

app_name = 'profiles'  

urlpatterns = [
    path('', homepage, name='home'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('edit/', EditProfileView.as_view(), name='edit'),
    path("edit/full/", views.EditProfileView.as_view(), name="edit_full"),
    path("edit/image/", views.EditProfileImageView.as_view(), name="edit_image"),
    path('profile/edit/full/', EditProfileView.as_view(), name='edit_profile'),
    path('edit-name-username/', views.edit_name_username, name='edit_name_username'),
]
