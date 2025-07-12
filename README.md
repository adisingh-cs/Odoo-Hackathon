# SkillExchange Django Backend

A traditional Django backend for the SkillExchange platform, built without Django REST Framework. This backend provides a complete web application with server-side rendering, forms, and session-based authentication.

## Features

### Core Functionality
- **User Management**: Registration, authentication, profiles, and user search
- **Skill Listings**: Create, edit, and manage skill offerings/requests
- **Swap System**: Request, accept, reject, and complete skill swaps
- **Messaging**: Private conversations and platform announcements
- **Reviews & Ratings**: Rate skills and swap experiences
- **Reporting System**: Report issues and track analytics
- **Admin Panel**: Comprehensive Django admin interface

### Technical Features
- **Traditional Django Views**: Function-based views with server-side rendering
- **Django Forms**: Form handling and validation
- **Session Authentication**: Standard Django authentication
- **File Uploads**: Profile pictures and media handling
- **Pagination**: Efficient data pagination
- **Search & Filtering**: Advanced search capabilities
- **Activity Logging**: Track user actions and system events

## Project Structure

```
skillexchange_django/
├── manage.py
├── requirements.txt
├── README.md
├── skillexchange/          # Main project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                  # User management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── skills/                 # Skill listings
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── swaps/                  # Swap system
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── messaging/              # Messaging system
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── reports/                # Reports & analytics
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/              # HTML templates (to be created)
├── static/                 # Static files (to be created)
└── media/                  # User uploads
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## Apps Overview

### Users App
- **Models**: Custom User, UserProfile, Notification
- **Features**: Registration, profile management, user search, notifications
- **Key Views**: Dashboard, profile, user list, notifications

### Skills App
- **Models**: Category, SkillListing, SkillReview
- **Features**: Skill creation, editing, reviews, categories
- **Key Views**: Skill list, detail, create/edit, reviews

### Swaps App
- **Models**: SwapRequest, SwapTransaction, SwapReview
- **Features**: Swap requests, acceptance/rejection, completion
- **Key Views**: Swap list, detail, create, manage requests

### Messaging App
- **Models**: Conversation, Message, PlatformMessage, UserMessageRead
- **Features**: Private messaging, platform announcements
- **Key Views**: Conversations, messages, platform announcements

### Reports App
- **Models**: Report, Analytics, UserActivity
- **Features**: Issue reporting, analytics, activity logging
- **Key Views**: Report creation, admin dashboard, analytics

## URL Structure

### Main URLs
- `/` - Home page
- `/login/` - Login
- `/register/` - Registration
- `/dashboard/` - User dashboard
- `/profile/` - User profile

### App URLs
- `/users/` - User management
- `/skills/` - Skill listings
- `/swaps/` - Swap system
- `/messaging/` - Messaging
- `/reports/` - Reports & analytics
- `/admin/` - Django admin

## Key Features

### Authentication & Authorization
- Custom User model with email as username
- Session-based authentication
- Login required decorators
- Staff-only views for admin functions

### Form Handling
- Django forms for all data input
- Form validation and error handling
- File upload support
- CSRF protection

### Database Design
- Comprehensive model relationships
- Proper foreign keys and many-to-many relationships
- Indexed fields for performance
- Audit trails with timestamps

### Admin Interface
- Full Django admin integration
- Custom admin classes for all models
- Search, filtering, and ordering
- Bulk actions and inline editing

## Development Notes

### Templates Required
This backend requires HTML templates to be created for:
- Base template with navigation
- User templates (login, register, profile, dashboard)
- Skill templates (list, detail, forms)
- Swap templates (list, detail, forms)
- Messaging templates (conversations, messages)
- Report templates (forms, admin views)

### Static Files
Create static files for:
- CSS styling
- JavaScript functionality
- Images and icons

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## Production Deployment

### Settings Changes
- Set `DEBUG = False`
- Configure production database (PostgreSQL recommended)
- Set up static file serving
- Configure email backend
- Set secure `SECRET_KEY`

### Security Considerations
- Use HTTPS in production
- Configure proper CORS settings
- Set up proper file upload handling
- Implement rate limiting
- Regular security updates

## API vs Traditional Django

This backend uses traditional Django patterns instead of REST Framework:

| Feature | Traditional Django | REST Framework |
|---------|-------------------|----------------|
| Views | Function-based views | ViewSets |
| Data Format | HTML forms | JSON API |
| Authentication | Session-based | JWT/Token |
| Rendering | Server-side | Client-side |
| Templates | Required | Optional |

## Next Steps

1. **Create Templates**: Build HTML templates for all views
2. **Add Static Files**: CSS, JavaScript, and images
3. **Testing**: Add unit tests and integration tests
4. **Frontend Integration**: Connect with your existing frontend
5. **Deployment**: Set up production environment

## 🚀 Project Lead

**Aditya Singh**  
- Role: Project Manager, Backend Developer (Django) 
- GitHub: [@adisingh-cs](https://github.com/adisingh-cs)

---

## 💡 Contributors

**[Dhruv Gupta]**  
- Role: Frontend Developer, UI/UX Designer  
- GitHub: [@Atheris29](https://github.com/Atheris29)

**[Anchal Maheshwari]**  
- Role: OCR Pipeline & PDF Handling
- GitHub: [@AnchalMaheshwari16](https://github.com/AnchalMaheshwari16)

**[Akanksha Gupta]**  
- Role: AI Integration,Easy OCR Integration, Documentation, Testing
- GitHub: [@Agupta163](https://github.com/Agupta163)
