from django.urls import path
from .views import Home, Authentication, LogoutView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Authentication.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]