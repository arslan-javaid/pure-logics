from django.urls import path
from .views import RackView, BookView, RackDetailView

urlpatterns = [
    path('rack/', RackView.as_view(), name='rack'),
    path('rack/<int:pk>', RackDetailView.as_view(), name='rack-detail'),
    path('book/', BookView.as_view(), name='book'),
]