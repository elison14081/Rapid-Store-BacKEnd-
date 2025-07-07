from django.urls import path
from .views import RegisterView, ProfileView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
