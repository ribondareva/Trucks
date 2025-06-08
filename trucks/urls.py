from django.urls import path
from .views import unload_view

urlpatterns = [
    path('', unload_view, name='unload'),
]
