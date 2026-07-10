from django.urls import path
from .views import start_simulation, stop_simulation, set_fault

urlpatterns = [
    path('start/', start_simulation),
    path('stop/', stop_simulation),
    path('fault/<str:name>/', set_fault),
]
