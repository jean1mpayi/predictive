from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorDataViewSet
from .views import latest_sensor
from .views_manual import (
    manual_update,
    manual_reset,
    manual_reset_all,
    manual_snapshot,
)


router = DefaultRouter()
router.register(r"sensors", SensorDataViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


urlpatterns += [
    path("latest/", latest_sensor),
]

# ------------------------------------------------------------------
# Manual Control endpoints
# ------------------------------------------------------------------
urlpatterns += [
    path("manual/update/",    manual_update),
    path("manual/reset/",     manual_reset),
    path("manual/reset_all/", manual_reset_all),
    path("manual/snapshot/",  manual_snapshot),
]