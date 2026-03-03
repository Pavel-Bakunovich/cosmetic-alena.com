# Cosmetic Alena - Flask Web Application

A professional, fully-featured Flask web application replica of the cosmetic-alena.com website. This is a complete beauty and cosmetic services website built with Flask, featuring appointment booking, service catalog, team profiles, and more.

## Features

✨ **Professional Design**
- Modern, responsive UI with gradient designs
- Mobile-first approach
- Smooth animations and transitions
- Professional color scheme (purple/gold gradient)

🛠️ **Complete Functionality**
- Service catalog with filtering
- Appointment booking system
- Contact form with email integration
- Newsletter subscription
- Team profiles
- Gallery
- Pricing pages with packages
- API endpoints for data access

💾 **Database Integration**
- SQLAlchemy ORM
- Services, Appointments, Contact Messages, Newsletter models
- Easy-to-extend database schema

🎨 **Modern Framework Stack**
- Flask
- Bootstrap 5
- jQuery
- Font Awesome icons
- Google Fonts (Playfair Display, Lato)

## Project Structure

```
cosmetic-alena.com/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js        # JavaScript functionality
│   │   └── images/            # Image assets
│   └── templates/
│       ├── base.html          # Base template
│       ├── index.html         # Home page
│       ├── services.html      # Services page
│       ├── pricing.html       # Pricing page
│       ├── team.html          # Team page
│       ├── gallery.html       # Gallery page
│       ├── about.html         # About page
│       ├── contact.html       # Contact page
│       ├── book-appointment.html  # Booking page
│       └── error pages (404, 500)
└── cosmetic_alena.db          # SQLite database (created on first run)
```

## Installation & Setup

### 1. Clone the Repository

```bash
cd /workspaces/cosmetic-alena.com
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file with your settings:

```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///cosmetic_alena.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. Initialize Database

The database will be created automatically on first run. To manually initialize:

```python
python3
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 6. Run the Application

```bash
python3 app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Home Page
Visit `http://localhost:5000/` to see the homepage with featured services and testimonials.

### Pages Available
- **Home** (`/`) - Featured services and welcome section
- **Services** (`/services`) - Complete service catalog with filtering
- **Pricing** (`/pricing`) - Service pricing and package details
- **Team** (`/team`) - Meet our beauty professionals
- **Gallery** (`/gallery`) - Portfolio of transformations
- **About** (`/about`) - Our story and values
- **Contact** (`/contact`) - Contact form and information
- **Book Appointment** (`/book-appointment`) - Appointment booking form

### API Endpoints

#### Services
- **GET** `/api/services` - Get all services
- **GET** `/api/services/<id>` - Get specific service

#### Appointments
- **GET** `/api/available-dates` - Get available dates
- **GET** `/api/available-times` - Get available times
- **POST** `/api/appointments` - Create new appointment
- **GET** `/api/appointments/<id>` - Get appointment details

#### Newsletter
- **POST** `/api/newsletter/subscribe` - Subscribe to newsletter

## Configuration

### Email Setup (Optional)

To enable email functionality:

1. For Gmail:
   - Generate an app-specific password: https://myaccount.google.com/apppasswords
   - Update `.env` with your Gmail and app password

2. Update `.env`:
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database

Change database in `.env`:

```bash
# SQLite (default)
DATABASE_URL=sqlite:///cosmetic_alena.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/cosmetic_alena

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost/cosmetic_alena
```

## Customization

### Add Services

To add services to the database:

```python
from app import app, db, Service

with app.app_context():
    service = Service(
        name="Facial Treatment",
        description="Professional facial treatment",
        price=79.99,
        duration=60,
        category="Skincare"
    )
    db.session.add(service)
    db.session.commit()
```

### Modify Colors

Edit `app/static/css/style.css`:

```css
:root {
    --primary-color: #667eea;      /* Change primary color */
    --primary-dark: #764ba2;       /* Change dark variant */
    --secondary-color: #D4AF37;    /* Change secondary color */
}
```

### Update Content

Edit the template files in `app/templates/` to change:
- Page content
- Headers and text
- Links and navigation
- Form fields

## Deployment

### For Production

1. Update `.env`:
```bash
FLASK_ENV=production
DEBUG=False
SECRET_KEY=generate-a-strong-secret-key
```

2. Use a production WSGI server:

```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using uWSGI
pip install uwsgi
uwsgi --http :8000 --wsgi-file app.py --callable app
```

3. Set up a reverse proxy (Nginx/Apache)

4. Enable HTTPS with SSL certificates

### Platform-Specific

**Heroku:**
```bash
heroku create cosmetic-alena
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

**Vercel/Netlify:** (Not ideal for Flask, use Heroku or traditional hosting)

**AWS/GCP/Azure:** Use their Flask/Python deployment guides

## Development

### Running Tests

```python
# Create tests in a tests/ directory
pytest
```

### Debugging

```bash
# Use Flask debugger
python3 -m flask run --debug

# Or set in app.py
app.run(debug=True)
```

### Working with the Database

```python
python3
>>> from app import app, db, Service
>>> with app.app_context():
...     services = Service.query.all()
...     for s in services:
...         print(s.name, s.price)
```

## Troubleshooting

### Port Already in Use
```bash
# Kill existing process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python3 app.py --port 8000
```

### Database Issues
```bash
# Delete database and recreate
rm cosmetic_alena.db
python3 app.py  # Recreates automatically
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Email Not Working
- Check credentials in `.env`
- Enable "Less secure app access" for Gmail (if not using app password)
- Check firewall/ISP blocking port 587

## Features Roadmap

- [ ] User authentication/login
- [ ] Client profiles and booking history
- [ ] Admin dashboard
- [ ] Payment integration (Stripe)
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Reviews and ratings
- [ ] Blog section
- [ ] Loyalty program

## Security

- CSRF protection enabled
- Secure session cookies
- Input validation and sanitization
- SQLAlchemy prevents SQL injection
- Environment variables for sensitive data

## Performance

- Responsive images
- Lazy loading
- CSS/JS minification ready
- Database indexing
- Caching headers configured

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This project is provided as-is for educational and commercial use.

## Support & Documentation

For issues, questions, or improvements:
1. Check the troubleshooting section
2. Review Flask documentation: https://flask.palletsprojects.com
3. Check Bootstrap 5 docs: https://getbootstrap.com/docs/5.0/

## Contact

For inquiries about this Flask application:
- Email: info@cosmetic-alena.com
- Website: https://cosmetic-alena.com

---

**Happy coding!** 🎉

Built with ❤️ using Flask, Bootstrap, and modern web technologies.
