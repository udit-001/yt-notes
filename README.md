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
8. Open your web browser and go to `http://127.0.0.1:8000/` to view the app.


## Running Tests

To run the tests for the application, use the following command:
```
python manage.py test app
```
