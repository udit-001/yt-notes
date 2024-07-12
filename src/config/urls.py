from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from app.views import *

urlpatterns = [
    path("", start_video, name="start-video"),
    path("video", watch_video, name="watch-video"),
    path('api/videos/', VideoCreateView.as_view(), name="video-create"),
    path('api/videos/<int:pk>/notes/', VideoNoteView.as_view(), name="note-list-create"),
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
