from django.contrib import admin
from django.urls import path

from billing_system.views.upload_csv_view import UploadCSVView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', UploadCSVView.as_view(), name='upload'),
]
