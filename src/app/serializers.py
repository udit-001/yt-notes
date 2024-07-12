from rest_framework import serializers

from .models import Note, Video
from .utils import validate_yt_url


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "url",
            "duration",
        ]

    def validate_url(self, value):
        session_id = self.context.get("request").session.session_key
        url_validity_check = validate_yt_url(value)

        if url_validity_check == True:
            query = Video.objects.filter(session_id=session_id, url=value)
            if query.exists():
                raise serializers.ValidationError(
                    "Given video already exists for current session"
                )
            else:
                return value
        else:
            raise serializers.ValidationError("This isn't a valid YouTube URL")


class VideoNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "content", "timestamp", "created_at"]

    def validate_timestamp(self, value):
        request = self.context.get("request")
        pk = request.parser_context.get("kwargs")["pk"]
        video = Video.objects.get(id=pk)

        if value <= video.duration:
            return value
        else:
            raise serializers.ValidationError(
                "Timestamp can't be greater than video duration"
            )
