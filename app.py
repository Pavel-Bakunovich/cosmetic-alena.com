"""
Cosmetic Alena - Flask Static Website
A professional cosmetics and beauty services website
"""

from flask import Flask, render_template
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='app/templates',
            static_folder='app/static', 
            static_url_path='/static')

services_path = os.path.join(
    os.path.dirname(__file__), 'app', 'config', 'cosmetic-services.json'
)
with open(services_path, encoding='utf-8') as services_file:
    SERVICES = json.load(services_file)

certificates_path = os.path.join(
    os.path.dirname(__file__), 'app', 'config', 'certificates.json'
)
with open(certificates_path, encoding='utf-8') as certificates_file:
    CERTIFICATES = json.load(certificates_file)

# Routes
@app.route('/')
def index():
    """Home page"""
    featured_services = SERVICES[:6]
    return render_template('index.html', featured_services=featured_services)

@app.route('/services')
def services():
    """Services page"""
    categories = list(set(s['category'] for s in SERVICES))
    return render_template('services.html', services=SERVICES, categories=categories)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/certificates')
def certificates():
    """Certificates page"""
    return render_template('certificates.html', certificates=CERTIFICATES)

@app.route('/gallery')
def gallery():
    """Gallery/Portfolio page"""
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/book-appointment')
def book_appointment():
    """Book appointment page"""
    return render_template('book-appointment.html', services=SERVICES)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Context processors
@app.context_processor
def inject_config():
    """Inject site configuration into templates"""
    return {
        'site_name': 'Косметик Алена',
        'site_tagline': 'Профессиональные услуги красоты и косметики',
        'year': datetime.utcnow().year,
        'services': SERVICES
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
