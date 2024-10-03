from django.contrib import admin
from django.urls import path

from .views import UploadCSVView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', UploadCSVView.as_view(), name='upload'),
]
