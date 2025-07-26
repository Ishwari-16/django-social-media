from django.urls import path
from .views import ProfileDetailView, FollowView, EditProfileView, homepage
from . import views

app_name = 'profiles'  

urlpatterns = [
    path('', homepage, name='home'),
    path('<str:username>/', ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('edit/', EditProfileView.as_view(), name='edit'),
    path("edit/full/", views.EditProfileView.as_view(), name="edit_full"),
    path("edit/", views.EditProfileView.as_view(), name="edit_profile"),
]
