from django.contrib import admin

from .models import Note, Video


class NoteInline(admin.StackedInline):
    model = Note
    extra = 0
    classes = ["collapse"]

    readonly_fields = ("created_at", "updated_at")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    inlines = [NoteInline]
    search_fields = ["title", "url"]
    readonly_fields = ["session_id"]


admin.site.site_title = "YouTube Notes App"
admin.site.index_title = "Manage Videos and Notes"
admin.site.site_header = "YouTube Notes Admin"
