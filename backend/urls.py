from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),
    path('simulation/', include('simulation.urls')),
    path("api/", include("api.urls")),
]

urlpatterns += staticfiles_urlpatterns()