from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Video, Note


class VideosTest(APITestCase):

    def setUp(self):
        self.session = self.client.session
        self.video_create_url = reverse("video-create")
        self.payload = {
            "title": "CS50W Lecture 0",
            "url": "https://www.youtube.com/watch?v=zFZrkCIc2Oc",
            "duration": 7412,
        }

    def test_video_create_success(self):
        create_response = self.client.post(
            self.video_create_url, format="json", data=self.payload
        )
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(
            create_response.headers.get("Content-Type"), "application/json"
        )

        self.assertEqual(create_response.data["url"], self.payload["url"])
        self.assertEqual(create_response.data["title"], self.payload["title"])
        self.assertEqual(create_response.data["duration"], self.payload["duration"])

    def test_video_create_invalid_url(self):
        data = self.payload.copy()
        data["url"] = "https://google.com"

        create_response = self.client.post(
            self.video_create_url, format="json", data=data
        )
        self.assertEqual(create_response.status_code, 400)
        self.assertEqual(
            create_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(
            create_response.json(), {"url": ["This isn't a valid YouTube URL"]}
        )

    def test_duplicate_video_create(self):
        create_response1 = self.client.post(
            self.video_create_url, format="json", data=self.payload
        )
        self.assertEqual(create_response1.status_code, 201)
        self.assertEqual(
            create_response1.headers.get("Content-Type"), "application/json"
        )

        # Data Check
        self.assertEqual(create_response1.data["url"], self.payload["url"])
        self.assertEqual(create_response1.data["title"], self.payload["title"])
        self.assertEqual(create_response1.data["duration"], self.payload["duration"])

        # Validation Check
        create_response2 = self.client.post(
            self.video_create_url, format="json", data=self.payload
        )
        self.assertEqual(create_response2.status_code, 400)
        self.assertEqual(
            create_response2.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(
            create_response2.json(),
            {"url": ["Given video already exists for current session"]},
        )


class NoteCreationTests(APITestCase):
    def setUp(self):
        self.session = self.client.session
        self.video_create_url = reverse("video-create")
        self.video_payload = {
            "title": "CS50W Lecture 0",
            "url": "https://www.youtube.com/watch?v=zFZrkCIc2Oc",
            "duration": 7412,
        }
        self.notes_create_payload = {"content": "This is some text", "timestamp": 3459}
        self.video_create_response = self.client.post(
            self.video_create_url, format="json", data=self.video_payload
        )
        self.video_id = self.video_create_response.data["id"]

    def test_note_create_success(self):
        notes_url = reverse("note-list-create", kwargs={"pk": self.video_id})
        notes_create_response = self.client.post(
            notes_url, format="json", data=self.notes_create_payload
        )
        self.assertEqual(notes_create_response.status_code, 201)
        self.assertEqual(
            notes_create_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(
            notes_create_response.json()["content"],
            self.notes_create_payload["content"],
        )
        self.assertEqual(
            notes_create_response.json()["timestamp"],
            self.notes_create_payload["timestamp"],
        )

    def test_note_create_for_nonexistent_video(self):
        notes_url = reverse("note-list-create", kwargs={"pk": 100})
        notes_create_response = self.client.post(
            notes_url, format="json", data=self.notes_create_payload
        )
        self.assertEqual(
            notes_create_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_create_response.json(), {"detail": "No Video matches the given query."})

    def test_note_create_invalid_timestamp(self):
        invalid_notes_create_payload = {
            "content": "This is some text",
            "timestamp": 7890,
        }
        notes_create_url = reverse("note-list-create", kwargs={"pk": self.video_id})
        notes_create_response = self.client.post(
            notes_create_url, format="json", data=invalid_notes_create_payload
        )
        self.assertEqual(notes_create_response.status_code, 400)
        self.assertEqual(
            notes_create_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(
            notes_create_response.json(),
            {"timestamp": ["Timestamp can't be greater than video duration"]},
        )

    def test_note_missing_content(self):
        invalid_notes_create_payload = {
            "timestamp": 3020,
        }
        notes_create_url = reverse("note-list-create", kwargs={"pk": self.video_id})
        notes_create_response = self.client.post(
            notes_create_url, format="json", data=invalid_notes_create_payload
        )
        self.assertEqual(
            notes_create_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_create_response.status_code, 400)
        self.assertEqual(
            notes_create_response.json(), {"content": ["This field is required."]}
        )

    def test_note_missing_timestamp(self):
        invalid_notes_create_payload = {"content": "this is some content"}
        notes_create_url = reverse("note-list-create", kwargs={"pk": self.video_id})
        notes_create_response = self.client.post(
            notes_create_url, format="json", data=invalid_notes_create_payload
        )
        self.assertEqual(
            notes_create_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_create_response.status_code, 400)
        self.assertEqual(
            notes_create_response.json(), {"timestamp": ["This field is required."]}
        )


class NotesRetrievalTests(APITestCase):
    def setUp(self):
        self.session_id = self.session = self.client.session.session_key
        self.video = Video.objects.create(
            title="This is the title",
            url="https://www.youtube.com/watch?v=zFZrkCIc2Oc",
            duration=349,
            session_id=self.session_id,
        )
        self.notes = [
            {
                "content": "First Content",
                "timestamp": 30,
            },
            {
                "content": "Third Content",
                "timestamp": 50,
            },
            {
                "content": "Second Content",
                "timestamp": 40,
            },
            {
                "content": "Fourth Content",
                "timestamp": 60,
            },
            {
                "content": "Fifth Content",
                "timestamp": 125,
            },
        ]
        for i in self.notes:
            Note.objects.create(
                video_id=self.video.id,
                content=i["content"],
                timestamp=i["timestamp"],
            )

    def test_notes_pagination_default(self):
        notes_url = reverse("note-list-create", kwargs={"pk": self.video.id})
        notes_list_response = self.client.get(notes_url, format="json")
        self.assertEqual(notes_list_response.status_code, 200)
        self.assertEqual(
            notes_list_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(len(notes_list_response.json()["results"]), len(self.notes))
        self.assertEqual(notes_list_response.json()["count"], len(self.notes))
        self.assertIsNone(notes_list_response.data["previous"])

    def test_notes_pagination_custom_limit(self):
        custom_limit = 2
        notes_url = reverse("note-list-create", kwargs={"pk": self.video.id})
        notes_url += f"?limit={custom_limit}"
        notes_list_response = self.client.get(notes_url, format="json")
        notes_list_data = notes_list_response.json()
        self.assertEqual(notes_list_response.status_code, 200)
        self.assertEqual(
            notes_list_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(len(notes_list_data["results"]), custom_limit)
        self.assertEqual(notes_list_data["count"], len(self.notes))
        self.assertIsNone(notes_list_data["previous"])
        self.assertEqual(
            notes_list_data["next"],
            f"http://testserver/api/videos/{self.video.id}/notes/?limit={custom_limit}&offset={custom_limit}",
        )

    def test_notes_ordering_default(self):
        # Default ordering is based on ascending timestamp
        notes_url = reverse("note-list-create", kwargs={"pk": self.video.id})
        notes_list_response = self.client.get(notes_url, format="json")
        notes_list_data = notes_list_response.json()
        self.assertEqual(notes_list_response.status_code, 200)
        self.assertEqual(
            notes_list_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_list_data["count"], len(self.notes))
        self.assertEqual(
            [note["content"] for note in notes_list_data["results"]],
            [
                "First Content",
                "Second Content",
                "Third Content",
                "Fourth Content",
                "Fifth Content",
            ],
        )

    def test_notes_ordering_by_timestamp_desc(self):
        notes_url = reverse("note-list-create", kwargs={"pk": self.video.id})
        notes_url += f"?ordering=-timestamp"
        notes_list_response = self.client.get(notes_url, format="json")
        notes_list_data = notes_list_response.json()
        self.assertEqual(notes_list_response.status_code, 200)
        self.assertEqual(
            notes_list_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_list_data["count"], len(self.notes))
        self.assertEqual(
            [note["content"] for note in notes_list_data["results"]],
            [
                "Fifth Content",
                "Fourth Content",
                "Third Content",
                "Second Content",
                "First Content",
            ],
        )

    def test_notes_ordering_by_creation_time_asc(self):
        notes_url = reverse("note-list-create", kwargs={"pk": self.video.id})
        notes_url += f"?ordering=created_at"
        notes_list_response = self.client.get(notes_url, format="json")
        notes_list_data = notes_list_response.json()
        self.assertEqual(notes_list_response.status_code, 200)
        self.assertEqual(
            notes_list_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_list_data["count"], len(self.notes))
        self.assertEqual(
            [note["content"] for note in notes_list_data["results"]],
            [
                "First Content",
                "Third Content",
                "Second Content",
                "Fourth Content",
                "Fifth Content",
            ],
        )

    def test_notes_ordering_by_creation_time_desc(self):
        notes_url = reverse("note-list-create", kwargs={"pk": self.video.id})
        notes_url += f"?ordering=-created_at"
        notes_list_response = self.client.get(notes_url, format="json")
        notes_list_data = notes_list_response.json()
        self.assertEqual(notes_list_response.status_code, 200)
        self.assertEqual(
            notes_list_response.headers.get("Content-Type"), "application/json"
        )
        self.assertEqual(notes_list_data["count"], len(self.notes))
        self.assertEqual(
            [note["content"] for note in notes_list_data["results"]],
            [
                "Fifth Content",
                "Fourth Content",
                "Second Content",
                "Third Content",
                "First Content",
            ],
        )
