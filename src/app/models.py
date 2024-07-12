from django.db import models
from django.utils import timezone


class Video(models.Model):
    session_id = models.CharField("session key", max_length=40)
    title = models.CharField(max_length=200)
    url = models.URLField()
    duration = models.PositiveIntegerField("Duration in seconds", null=True, blank=True)

    class Meta:
        unique_together = (
            "session_id",
            "url",
        )

    def __str__(self):
        return self.title


class Note(models.Model):
    video = models.ForeignKey(Video, related_name="notes", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.PositiveIntegerField("Timestamp in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]
