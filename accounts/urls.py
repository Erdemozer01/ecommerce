from django.urls import path
from accounts.views import UserRegister, ProfileUpdateView, UserDeleteView

app_name = "accounts"

urlpatterns = [
    path('register/', UserRegister.as_view(), name="register"),
    path('user-profil/<str:user>/', ProfileUpdateView, name='profile_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
]
