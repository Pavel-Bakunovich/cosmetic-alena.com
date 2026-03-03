# Cosmetic Alena - Flask Static Website

A professional Flask web application that serves a static beauty and cosmetics services website, featuring:
- Professional styling with Bootstrap 5
- Service catalog with pricing
- Beautiful gallery and portfolio
- Team member profiles
- Contact and appointment booking forms
- Responsive design for all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup & Run

#### On Linux/Mac (using quickstart.sh)
```bash
chmod +x quickstart.sh
./quickstart.sh
python3 app.py
```

#### On Windows (using quickstart.bat)
```bash
quickstart.bat
python app.py
```

#### Manual Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python3 app.py
```

Then open your browser and visit: **http://localhost:5000**

## 📁 Project Structure

```
cosmetic-alena.com/
├── app.py                 # Main Flask application
├── app/
│   ├── templates/         # HTML templates (11 pages)
│   │   ├── base.html      # Master template
│   │   ├── index.html     # Home page
│   │   ├── services.html  # Services catalog
│   │   ├── pricing.html   # Pricing table
│   │   ├── team.html      # Team profiles
│   │   ├── gallery.html   # Portfolio gallery
│   │   ├── about.html     # About page
│   │   ├── contact.html   # Contact form
│   │   ├── book-appointment.html  # Booking form
│   │   ├── 404.html       # Error page
│   │   └── 500.html       # Server error
│   └── static/
│       ├── css/style.css          # Professional styling
│       └── js/main.js             # Form & interactivity
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (auto-generated)
└── README.md             # This file
```

## 🎨 Features

- **Responsive Design**: Looks great on all devices (mobile, tablet, desktop)
- **Service Management**: View all 12 beauty services with pricing and duration
- **Category Filtering**: Services organized by category (Skincare, Makeup, Hair, etc.)
- **Team Profiles**: Meet the professional team members
- **Contact & Booking**: Forms for inquiries and appointment bookings
- **Professional Styling**: Modern UI with Bootstrap 5 and custom CSS
- **No Database Required**: Static content - can be easily deployed anywhere

## 🛠️ Technologies Used

- **Flask 2.3.2** - Web framework
- **Jinja2** - Template engine
- **Bootstrap 5** - UI framework
- **jQuery** - JavaScript library
- **Font Awesome** - Icon library
- **Python-dotenv** - Configuration management

## 📝 Services Included

The website features 12 beauty services across 6 categories:
- **Skincare**: Facial Treatment, Deep Cleansing Peel
- **Makeup**: Makeup Application, Bridal Makeup, Eyelash Extensions  
- **Hair**: Hair Styling, Hair Coloring
- **Grooming**: Eyebrow Threading, Waxing Services
- **Wellness**: Relaxation Massage, Body Treatment
- **Nails**: Nail Art & Extensions

## 👥 Team

The website showcases 6 professional team members:
- Alena Viktoria - Founder & Lead Aesthetician
- Maria Svetlova - Senior Makeup Artist
- Natalia Petrov - Skincare Specialist
- Dmitri Sokolov - Hair & Grooming Expert
- Yuliana Orlova - Nail & Extension Specialist
- Anna Volkova - Wellness & Spa Manager

## 🌐 Routes

- `/` - Home page with featured services
- `/services` - Complete service catalog with filtering
- `/pricing` - Service pricing table  
- `/team` - Team member profiles
- `/about` - About the business
- `/gallery` - Portfolio gallery
- `/contact` - Contact form
- `/book-appointment` - Appointment booking form

## 💾 Data Storage

All data is stored statically in `app.py`:
- Services list with 12 pre-configured services
- Team members with bios and titles
- Contact/booking forms show success message (client-side only)

## 🚀 Deployment

This Flask app can be deployed to any Python hosting platform:
- Heroku
- PythonAnywhere
- AWS/Google Cloud
- Azure
- Docker container
- Traditional VPS

For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app:app
```

## 📚 Additional Documentation

- **SETUP_AND_RUN.md** - Detailed setup instructions
- **COMPLETE_DOCUMENTATION.md** - Full project documentation
- **app.py** - Source code with comments

## 📄 License

This is a replica project for learning purposes.

## 🤝 Support

For issues or questions about the Flask application, check the source code in app.py which includes helpful comments.
python3 fetch_website.py

# Detailed analysis
python3 analyze_website.py
```

## 📚 Documentation Files

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **README_ANALYSIS_PACKAGE.md** | Overview & package contents | 5 min |
| **QUICK_START.md** | Quick reference guide | 5 min |
| **ANALYSIS_README.md** | Tool usage guide | 10 min |
| **EXTRACTION_GUIDE.md** | What gets extracted | 15 min |
| **FLASK_IMPLEMENTATION_GUIDE.md** | Build Flask app | 20 min |

## 🎯 Project Goals

- ✅ Analyze complete website structure
- ✅ Extract all resources (CSS, JS, images)
- ✅ Identify page components and layout
- ✅ Extract all text content and forms
- ✅ Map navigation and links
- ✅ Generate comprehensive reports
- ✅ Provide Flask implementation examples
- ✅ Create reusable templates and components

## 📊 What Gets Extracted

- Page structure and layout
- All CSS stylesheets
- All JavaScript files
- All images and media
- Navigation links and structure
- Forms and input fields
- Text content and headings
- Color schemes
- API endpoints
- Metadata and SEO info

## 🛠️ Generated Reports

After running analysis, you'll get:

- `website_full.html` - Raw HTML
- `website_pretty.html` - Formatted HTML
- `analysis_report.json` - Structured data
- `WEBSITE_ANALYSIS.md` - Human-readable report
- `website_content/` - All downloaded resources (if using advanced_analyzer.py)

## 🚀 Build Your Flask App

The **FLASK_IMPLEMENTATION_GUIDE.md** includes:
- Complete Flask application structure
- HTML template examples
- Database models
- API endpoint examples
- Form handlers
- Configuration management

## 📋 Requirements

```bash
pip install requests beautifulsoup4
```

## ⚙️ Project Structure

```
/workspaces/cosmetic-alena.com/
├── *.py                              # Analysis scripts
├── README.md                         # This file
├── README_ANALYSIS_PACKAGE.md        # Package overview
├── QUICK_START.md                    # Quick reference
├── ANALYSIS_README.md                # Tool guide
├── EXTRACTION_GUIDE.md               # Data extraction details
├── FLASK_IMPLEMENTATION_GUIDE.md     # Flask app guide
├── app/                              # Flask app directory (to be created)
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
└── website_content/                  # Extracted resources (optional)
    ├── html/
    ├── css/
    ├── js/
    └── images/
```

## 🎓 How to Use This Package

### Option A: Quick Analysis (Recommended for beginners)
```bash
python3 comprehensive_analysis.py
cat WEBSITE_ANALYSIS.md
```

### Option B: Complete Extraction (Recommended for implementation)
```bash
python3 advanced_analyzer.py
# Navigate to website_content/ to see all downloads
```

### Option C: Just Get Started
```bash
# Read the guides in this order
1. README_ANALYSIS_PACKAGE.md
2. QUICK_START.md
3. FLASK_IMPLEMENTATION_GUIDE.md
```

## 📚 Next Steps

1. **Analyze** - Run analysis script to extract data
2. **Learn** - Read the documentation
3. **Plan** - Map out your Flask routes and pages
4. **Code** - Create Flask app based on extracted data
5. **Style** - Copy and customize CSS
6. **Build** - Add forms and interactive features
7. **Test** - Verify all functionality
8. **Deploy** - Host your Flask app

## 🤝 Contributing

This is a learning/development project. Feel free to:
- Modify and improve the analysis scripts
- Add new extraction features
- Improve documentation
- Create additional tools

## ⚠️ Important Notes

- This analysis is for educational and development purposes
- Respect original website's copyright and intellectual property
- When deploying, create your own original content
- Test thoroughly before going live
- Consider legal implications of website replication

## 📞 Support

- Check **QUICK_START.md** for troubleshooting
- Review inline documentation in Python scripts
- Consult **EXTRACTION_GUIDE.md** for data format questions
- See **FLASK_IMPLEMENTATION_GUIDE.md** for coding questions

## 📅 Last Updated

March 3, 2026 - Complete analysis package with tools and documentation ready for use

---

**Status:** ✅ Ready to analyze and build Flask replica of cosmetic-alena.com
