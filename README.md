# News Application

A Django-based news publishing platform that allows journalists to create articles, editors to review and approve content, and readers to subscribe and read news.

## Features

### User Roles
- **Readers**: Browse and read approved articles, subscribe to journalists
- **Journalists**: Create articles and newsletters, manage their content
- **Editors**: Review, approve, and manage all content

### Core Functionality
- Article creation and management
- Newsletter system
- Content approval workflow
- User authentication and authorization
- Email notifications
- Twitter integration
- REST API endpoints

## Installation & Setup

### Prerequisites
- Python 3.8+
- SQLite database (default) or MariaDB/MySQL
- Virtual environment
- Docker (optional, for containerized deployment)

## Local Development (with Virtual Environment)

1. Clone the repository:
   ```bash
   git clone https://github.com/DioneLearns/literate-octo-journey.git
   cd news_application
Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Run migrations:

bash
python manage.py migrate
Create superuser (optional):

bash
python manage.py createsuperuser
Run development server:

bash
python manage.py runserver
Visit http://localhost:8000 in your browser.

Running with Docker
Build the Docker image:

bash
docker build -t news-app .
Run the container:

bash
docker run -d -p 8000:8000 --name news-container news-app
Visit http://localhost:8000 in your browser.

To stop the container:

bash
docker stop news-container
Usage
For Readers
Register as a reader

Browse articles on the home page

Click "Read More" to view full articles

Subscribe to journalists for updates

For Journalists
Register as a journalist

Create articles and newsletters

Wait for editor approval

Manage your content in "My Articles"

For Editors
Access admin panel at /admin/

Review pending articles at /news/approve/

Approve or reject content

Manage users and publishers

API Endpoints
The application includes REST API endpoints accessible at /api/ for programmatic access to news content.

Configuration
Key settings in news_project/settings.py:

Database configuration (SQLite default, MariaDB/MySQL optional)

Email settings for notifications

Twitter API integration

Static files configuration

Documentation
Project documentation is built with Sphinx. To regenerate:

bash
cd docs
make html
Open docs/build/html/index.html in your browser.
