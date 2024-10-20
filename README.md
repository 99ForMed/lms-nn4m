# lms-nn4m

A robust Learning Management System (LMS) built with Django, featuring real-time class management, forums, user authentication, and more. This project is designed to support interactive learning through real-time sessions using websocket technology.

## Features
- **User Authentication**: Secure login and registration system.
- **Live Classes**: Real-time class sessions with websocket support for interactive learning.
- **Forum**: Community-driven discussion forums.
- **Interview Module**: Tools for conducting and managing mock interviews.
- **Admin Interface**: Django’s built-in admin for managing courses, users, and content.

## Technologies
- **Backend**: Django, Django Channels for websocket integration.
- **Frontend**: HTML, CSS, JavaScript for dynamic content.
- **Database**: SQLite (development), PostgreSQL (production).
- **Deployment**: Includes a `Procfile` for deployment on platforms like Heroku.

## Getting Started

### Prerequisites
- Python 3.x
- Django 4.x
- Any required packages in `requirements.txt`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/callmepri/lms-nn4m.git
   cd lms-nn4m
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Directory Structure
- `authentication/`: Manages user sign-up, login, and session management.
- `forum/`: Contains logic for user-created posts and discussions.
- `live_class/`: Websocket-based logic for real-time class sessions.
- `interview/`: Handles the structure and flow of mock interviews.
- `nnlms/`: Core settings, URLs, and configurations.
- `static/` & `templates/`: Static assets and template files for rendering the front end.

## Websocket Integration
- The project uses **Django Channels** to manage websockets, enabling real-time communication between clients and the server.
- Websockets are used in `live_class/` for managing real-time interactions during class sessions.

## Deployment
- Use the `Procfile` for deployment to Heroku:
   ```bash
   web: gunicorn nnlms.wsgi --log-file -
   ```
- Ensure environment variables are set correctly for the database and other services in production.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any new features or bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
