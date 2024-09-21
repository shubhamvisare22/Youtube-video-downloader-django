from django.urls import path
from .views import DownloadView, home, DownloadFileView

urlpatterns = [
    path("download", DownloadView.as_view(), name="download"),
    path("download_video", DownloadFileView.as_view(), name="download_video"),
    path("", home, name="home"),
]
