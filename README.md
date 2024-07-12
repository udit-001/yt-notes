## Requirements
This app requires Python 3.10 or higher, up to version 3.12.

## Installation
To install the, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/udit-001/yt-notes.git
   ```
2. Change into the project directory:
   ```bash
   cd yt-notes
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
6. Run the Django migrations:
   ```
   python manage.py migrate
   ```
7. Start the Django development server:
   ```
   python manage.py runserver
   ```


## Running Tests

To run the tests for the application, use the following command:
```
python manage.py test app
```

## API Documentation

The API documentation for this app can be accessed at http://localhost:8000/api/docs/

### API Endpoints

The following API endpoints are available:

#### Create a new video

To create a new video, send a POST request to `/api/videos/` with the following payload:

```json
{
    "title": "Video title",
    "url": "https://www.youtube.com/watch?v=ABCDEFGHIJ",
    "duration": 120
}
```

Note:
- The url field must be a valid YouTube URL.
- The duration field must be an integer representing the length of the video in seconds.


* `/api/videos/` (POST): Create a new video for the current session
* `/api/videos/<int:pk>/notes/` (GET, POST): List all notes for a video or create a new note.


#### Create a new note
To create a new note, send a POST request to `/api/videos/<int:pk>/notes/` with the following payload:

```json
{
  "content": "Note content",
  "timestamp": 12345
}
```

Note:
- The timestamp field is an integer representing a point in time in the video where the note was added, it should be less than or equal to the duration of the video.
- `<int:pk>` is the id of the video returned by the `/api/videos/` endpoint as response. Eg: `/api/videos/3/notes/`
