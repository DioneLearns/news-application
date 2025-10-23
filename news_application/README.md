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
- MariaDB/MySQL database
- Virtual environment

### Quick Start
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python setup_mariadb.py
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver


### Usage
# For Readers
Register as a reader
Browse articles on the home page
Click "Read More" to view full articles
Subscribe to journalists for updates

# For Journalists
Register as a journalist
Create articles and newsletters
Wait for editor approval
Manage your content in "My Articles"

# For Editors
Access admin panel at /admin/
Review pending articles at /news/approve/
Approve or reject content
Manage users and publishers

# API Endpoints
The application includes REST API endpoints accessible at /api/ for programmatic access to news content.

# Configuration
Key settings in news_project/settings.py:
Database configuration (MariaDB/MySQL)
Email settings for notifications
Twitter API integration
Static files configuration

