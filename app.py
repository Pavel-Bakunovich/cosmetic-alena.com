"""
Cosmetic Alena - Flask Static Website
A professional cosmetics and beauty services website
"""

from flask import Flask, render_template
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='app/templates',
            static_folder='app/static', 
            static_url_path='/static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cosmetic-alena-static-site')

# Static data for services
SERVICES = [
    {
        'id': 1,
        'name': 'Процедура для лица',
        'description': 'Профессиональная европейская процедура для лица с премиальными косметическими продуктами. Включает очищение, пилинг, экстракцию, массаж и увлажняющую маску.',
        'price': 89.99,
        'duration': 60,
        'category': 'Уход за кожей'
    },
    {
        'id': 2,
        'name': 'Нанесение макияжа',
        'description': 'Профессиональное нанесение макияжа на любой случай. Экспертный подбор цвета и техника для безупречного результата.',
        'price': 59.99,
        'duration': 45,
        'category': 'Макияж'
    },
    {
        'id': 3,
        'name': 'Укладка волос',
        'description': 'Точный срез и профессиональная укладка. Включает консультацию, стрижку и укладку феном.',
        'price': 75.00,
        'duration': 60,
        'category': 'Волосы'
    },
    {
        'id': 4,
        'name': 'Свадебный макияж',
        'description': 'Полный пакет свадебного макияжа с пробной сессией. Долговечный профессиональный макияж для свадебного дня.',
        'price': 150.00,
        'duration': 90,
        'category': 'Макияж'
    },
    {
        'id': 5,
        'name': 'Дизайн и наращивание ногтей',
        'description': 'Творческие дизайны ногтей с гель-лаком или наращиванием. Профессиональное применение и уход за кутикулой.',
        'price': 65.00,
        'duration': 90,
        'category': 'Ногти'
    },
    {
        'id': 6,
        'name': 'Нитевое выщипывание бровей',
        'description': 'Точное моделирование бровей. Включает окрашивание для ухоженного вида.',
        'price': 25.00,
        'duration': 30,
        'category': 'Уход и красота'
    },
    {
        'id': 7,
        'name': 'Глубокий очищающий пилинг',
        'description': 'Химический пилинг для обновления и осветления кожи. Улучшает текстуру и тон кожи.',
        'price': 120.00,
        'duration': 75,
        'category': 'Уход за кожей'
    },
    {
        'id': 8,
        'name': 'Релаксирующий массаж',
        'description': 'Полный массаж расслабления для всего тела. Шведские техники массажа для облегчения напряжения и стресса.',
        'price': 99.99,
        'duration': 60,
        'category': 'Оздоровление'
    },
    {
        'id': 9,
        'name': 'Наращивание ресниц',
        'description': 'Роскошное наращивание ресниц. Добавляет объем и длину для драматичного вида.',
        'price': 110.00,
        'duration': 120,
        'category': 'Макияж'
    },
    {
        'id': 10,
        'name': 'Окрашивание волос',
        'description': 'Профессиональная услуга по окрашиванию волос. Окрашивание корней, полное окрашивание, мелирование или балаяж.',
        'price': 95.00,
        'duration': 90,
        'category': 'Волосы'
    },
    {
        'id': 11,
        'name': 'Уход за телом',
        'description': 'Роскошный скраб для тела и процедура увлажнения. Включает пилинг и увлажняющее нанесение.',
        'price': 85.00,
        'duration': 60,
        'category': 'Оздоровление'
    },
    {
        'id': 12,
        'name': 'Услуги депиляции воском',
        'description': 'Профессиональная депиляция воском. Доступна для лица, ног, рук и других областей.',
        'price': 45.00,
        'duration': 45,
        'category': 'Уход и красота'
    },
]

TEAM_MEMBERS = [
    {
        'name': 'Алена Виктория',
        'title': 'Основатель и главный косметолог',
        'bio': 'Обладая более чем 15-летним опытом в сфере красоты и косметики, Алена основала эту студию для предоставления первоклассных услуг красоты.'
    },
    {
        'name': 'Мария Светлова',
        'title': 'Старший визажист',
        'bio': 'Специалист по свадебному макияжу и цветокоррекции. Сертифицированный и награждённый визажист с международным признанием.'
    },
    {
        'name': 'Наталья Петрова',
        'title': 'Специалист по уходу за кожей',
        'bio': 'Эксперт в уходе за лицом и косметических решениях. Обучена европейским протоколам красоты с акцентом на натуральные и устойчивые методы.'
    },
    {
        'name': 'Дмитрий Соколов',
        'title': 'Эксперт по волосам и уходу',
        'bio': 'Профессиональный стилист с опытом в современных стрижках и окрашивании. Специалист как для мужского, так и для женского ухода за волосами.'
    },
    {
        'name': 'Юлиана Орлова',
        'title': 'Специалист по ногтям и наращиванию',
        'bio': 'Эксперт в искусстве ногтей и техниках наращивания. Специалист по последним тенденциям и здоровью ногтей с художественным чувством.'
    },
    {
        'name': 'Анна Волкова',
        'title': 'Менеджер оздоровительного спа',
        'bio': 'Создание комплексного опыта красоты через оздоровительные процедуры и спа-терапии. Сертифицированный массажист и консультант по оздоровлению.'
    },
]

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

@app.route('/gallery')
def gallery():
    """Gallery/Portfolio page"""
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html', services=SERVICES)

@app.route('/team')
def team():
    """Team page"""
    return render_template('team.html', team_members=TEAM_MEMBERS)

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
        'services': SERVICES,
        'team': TEAM_MEMBERS
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
