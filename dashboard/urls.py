from django.urls import path
from .views import dashboard_view, alerts_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('alerts/', alerts_view, name='alerts_list'),
]