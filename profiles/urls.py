from django.urls import path
from .views import ProfileDetailView, FollowView, EditProfileView, homepage

app_name = 'profiles'  

urlpatterns = [
    path('', homepage, name='home'),
    path('<str:username>/', ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('edit/', EditProfileView.as_view(), name='edit'),
]
