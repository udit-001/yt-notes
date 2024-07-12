from rest_framework import exceptions, filters, generics

from .models import *
from .serializers import *


class VideoCreateView(generics.CreateAPIView):
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save(session_id=self.request.session.session_key)


class VideoNoteView(generics.ListCreateAPIView):
    serializer_class = VideoNoteSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "timestamp"]
    search_fields = ["content"]

    def get_queryset(self):
        session_id = self.request.session.session_key
        videos = Video.objects.filter(session_id=session_id)
        video_id = self.request.parser_context["kwargs"]["pk"]

        if not videos.filter(id=video_id).exists():
            exceptions.NotFound()

        return (
            Note.objects.select_related("video")
            .filter(video_id=video_id, video__session_id=session_id)
            .order_by("timestamp")
        )

    def create(self, request, pk, *args, **kwargs):
        video_id = self.kwargs.get("pk")
        queryset = Video.objects.filter(session_id=self.request.session.session_key)
        video = generics.get_object_or_404(queryset, id=video_id)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        video_id = self.request.parser_context["kwargs"]["pk"]
        video = Video.objects.get(id=video_id)
        serializer.save(video=video)
