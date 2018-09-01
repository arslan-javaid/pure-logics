from django.urls import path
from .views import RackView, BookView

urlpatterns = [
    path('rack/', RackView.as_view(), name='rack'),
    path('book/', BookView.as_view(), name='book'),
]