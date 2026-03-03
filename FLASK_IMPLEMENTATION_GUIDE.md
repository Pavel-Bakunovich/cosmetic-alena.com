# Flask Replica Implementation Guide

## Overview

After analyzing cosmetic-alena.com, you'll have all the data needed to create a Flask-based replica. This document guides you through the implementation process.

## Directory Structure

```
flask_cosmetic_app/
├── app.py                      # Flask application main file
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── static/
│   ├── css/
│   │   └── style.css          # Define custom styles here
│   ├── js/
│   │   └── main.js            # Custom JavaScript
│   ├── images/                # Copy images here
│   └── fonts/                 # Custom fonts if needed
├── templates/
│   ├── base.html              # Base template with header/footer
│   ├── index.html             # Home page
│   ├── services.html          # Services page
│   ├── about.html             # About page
│   ├── contact.html           # Contact page
│   ├── gallery.html           # Portfolio/gallery page
│   └── 404.html               # Error page
└── data/
    └── site_content.json      # Content configuration
```

## Step 1: Extract Website Data

Run the analysis scripts to extract all information:

```bash
# Comprehensive analysis
python3 comprehensive_analysis.py

# Or advanced analysis with downloads
python3 advanced_analyzer.py
```

This generates:
- `analysis_report.json` - Detailed resource list
- `WEBSITE_ANALYSIS.md` - Human-readable analysis  
- `website_content/` - Downloaded resources

## Step 2: Create Flask Application

### app.py

```python
from flask import Flask, render_template, request, jsonify, send_from_directory
import json
from pathlib import Path

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['JSON_SORT_KEYS'] = False

# Load site configuration from analysis
with open('data/site_content.json', 'r') as f:
    SITE_CONFIG = json.load(f)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', config=SITE_CONFIG)

@app.route('/services')
def services():
    """Services page"""
    return render_template('services.html', config=SITE_CONFIG)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', config=SITE_CONFIG)

@app.route('/gallery')
def gallery():
    """Gallery/Portfolio page"""
    return render_template('gallery.html', config=SITE_CONFIG)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handler"""
    if request.method == 'POST':
        # Handle form submission
        data = request.get_json() or request.form
        
        # Validate data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        if not all([name, email, message]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Process contact form
        # TODO: Send email, save to database, etc.
        
        return jsonify({'success': True, 'message': 'Message received'}), 200
    
    return render_template('contact.html', config=SITE_CONFIG)

@app.route('/api/appointments', methods=['GET', 'POST'])
def api_appointments():
    """API endpoint for appointments"""
    if request.method == 'POST':
        data = request.get_json()
        # TODO: Save appointment to database
        return jsonify({'success': True, 'id': 1}), 201
    
    # Return list of available slots
    return jsonify({'slots': []}), 200

@app.route('/api/services')
def api_services():
    """API endpoint for services"""
    return jsonify(SITE_CONFIG.get('services', []))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### config.py

```python
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### requirements.txt

```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Mail==0.9.1
Flask-WTF==1.1.1
python-dotenv==1.0.0
requests==2.31.0
```

### .env (example)

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Step 3: Create HTML Templates

### templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ config.description }}">
    <title>{% block title %}{{ config.title }}{% endblock %}</title>
    
    <!-- Bootstrap CSS (or other framework) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header -->
    <header class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="/">{{ config.business_name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <nav class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="/services">Services</a></li>
                    <li class="nav-item"><a class="nav-link" href="/gallery">Gallery</a></li>
                    <li class="nav-item"><a class="nav-link" href="/about">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="min-vh-100">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>{{ config.business_name }}</h5>
                    <p>{{ config.tagline }}</p>
                </div>
                <div class="col-md-4">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="/" class="text-white-50">Home</a></li>
                        <li><a href="/services" class="text-white-50">Services</a></li>
                        <li><a href="/contact" class="text-white-50">Contact</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>Contact Info</h5>
                    <p><a href="tel:{{ config.phone }}" class="text-white-50">{{ config.phone }}</a></p>
                    <p><a href="mailto:{{ config.email }}" class="text-white-50">{{ config.email }}</a></p>
                </div>
            </div>
            <hr class="bg-white-50">
            <p class="text-center text-white-50">© 2024 {{ config.business_name }}. All rights reserved.</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### templates/index.html

```html
{% extends "base.html" %}

{% block title %}Home - {{ config.business_name }}{% endblock %}

{% block content %}
<section class="hero-section" style="background: url({{ url_for('static', filename='images/hero.jpg') }}) center/cover;">
    <div class="container h-100 d-flex align-items-center">
        <div class="text-center text-white">
            <h1 class="display-4 mb-4">{{ config.hero_title }}</h1>
            <p class="lead mb-4">{{ config.hero_subtitle }}</p>
            <a href="/contact" class="btn btn-primary btn-lg">Book Appointment</a>
        </div>
    </div>
</section>

<section class="services-section py-5">
    <div class="container">
        <h2 class="text-center mb-4">{{ config.services_title }}</h2>
        <div class="row">
            {% for service in config.services %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="{{ url_for('static', filename='images/' + service.image) }}" class="card-img-top" alt="{{ service.name }}">
                    <div class="card-body">
                        <h5 class="card-title">{{ service.name }}</h5>
                        <p class="card-text">{{ service.description }}</p>
                        <p class="text-muted">${{ service.price }}</p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```

### templates/contact.html

```html
{% extends "base.html" %}

{% block title %}Contact - {{ config.business_name }}{% endblock %}

{% block content %}
<section class="contact-section py-5">
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <h2>Get in Touch</h2>
                <form id="contactForm" method="POST">
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone</label>
                        <input type="tel" class="form-control" id="phone" name="phone">
                    </div>
                    <div class="mb-3">
                        <label for="message" class="form-label">Message</label>
                        <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
            <div class="col-md-6">
                <h2>Contact Info</h2>
                <p>
                    <strong>Address:</strong><br>
                    {{ config.address }}
                </p>
                <p>
                    <strong>Phone:</strong><br>
                    <a href="tel:{{ config.phone }}">{{ config.phone }}</a>
                </p>
                <p>
                    <strong>Email:</strong><br>
                    <a href="mailto:{{ config.email }}">{{ config.email }}</a>
                </p>
                <p>
                    <strong>Hours:</strong><br>
                    {{ config.hours }}
                </p>
            </div>
        </div>
    </div>
</section>
{% endblock %}

{% block extra_js %}
<script>
document.getElementById('contactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    const response = await fetch('/contact', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    
    if (response.ok) {
        alert('Message sent successfully!');
        e.target.reset();
    } else {
        alert('Error sending message. Please try again.');
    }
});
</script>
{% endblock %}
```

## Step 4: Create Content Configuration

### data/site_content.json

```json
{
  "title": "Cosmetic Alena",
  "business_name": "Cosmetic Alena",
  "description": "Professional cosmetic services and treatments",
  "tagline": "Your beauty is our passion",
  "logo": "/static/images/logo.png",
  "hero_title": "Discover Your Best Self",
  "hero_subtitle": "Professional cosmetic services for everyone",
  "phone": "+1-XXX-XXX-XXXX",
  "email": "info@cosmetic-alena.com",
  "address": "123 Beauty Street, City, State 12345",
  "hours": "Mon-Fri: 9AM-6PM, Sat: 10AM-4PM",
  "services": [
    {
      "id": 1,
      "name": "Facial Treatments",
      "description": "Professional facial treatments for all skin types",
      "price": 75,
      "image": "facial.jpg"
    },
    {
      "id": 2,
      "name": "Hair Services",
      "description": "Expert hair care and styling",
      "price": 50,
      "image": "hair.jpg"
    },
    {
      "id": 3,
      "name": "Nail Services",
      "description": "Manicures and pedicures",
      "price": 35,
      "image": "nails.jpg"
    }
  ]
}
```

## Step 5: Run the Flask Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the app
python3 app.py
```

Visit http://localhost:5000 to see your Flask replica!

## Step 6: Customize and Deploy

1. **Customize CSS** - Edit `static/css/style.css` to match the original design
2. **Add Images** - Copy extracted images to `static/images/`
3. **Implement Backend** - Add database, email, authentication as needed
4. **Deploy** - Use Gunicorn, Heroku, AWS, or your preferred platform

## Common API Endpoints to Implement

Based on website analysis, create these endpoints:

```python
# Appointments
GET    /api/appointments      - Get available slots
POST   /api/appointments      - Book appointment
GET    /api/appointments/<id> - Get appointment details
DELETE /api/appointments/<id> - Cancel appointment

# Services
GET    /api/services          - Get all services
GET    /api/services/<id>     - Get service details

# Testimonials
GET    /api/testimonials      - Get customer reviews

# Contact/Messages
POST   /api/messages          - Submit contact form
```

## Additional Features to Consider

- Email notifications for form submissions
- Database models for appointments, services, testimonials
- User authentication for client bookings
- Admin panel for managing content
- Image gallery with lightbox
- Testimonials management
- SEO optimization
- Mobile responsiveness
- Analytics integration

---

This structure provides a solid foundation for your Flask-based cosmetic services website replica!
