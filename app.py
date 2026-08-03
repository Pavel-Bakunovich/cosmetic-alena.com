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
        'name': 'Пробный сеанс',
        'description': 'Попробвать в первый раз',
        'price': 40.00,
        'duration': 25,
        'category': 'Биомеханическая стимуляция (БМС)'
    },
    {
        'id': 2,
        'name': 'Один сеанс',
        'description': 'Одна процедура БМС',
        'price': 65.00,
        'duration': 50,
        'category': 'Биомеханическая стимуляция (БМС)'
    },
    {
        'id': 3,
        'name': 'Курс',
        'description': '10 сеансов',
        'price': 600.00,
        'duration': 500,
        'category': 'Биомеханическая стимуляция (БМС)'
    },
    {
        'id': 4,
        'name': 'Ультразвуковая чистка лица',
        'description': 'Чистка лица с использованием ультразвуковых технологий для удаления загрязнений и улучшения текстуры кожи.',
        'price': 70.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 5,
        'name': 'Механическая чистка лица',
        'description': 'Чистка лица с использованием механических методов для удаления загрязнений и улучшения текстуры кожи.',
        'price': 90.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 6,
        'name': 'Комбинированная чистка лица',
        'description': 'Чистка лица с использованием комбинированных методов для удаления загрязнений и улучшения текстуры кожи.',
        'price': 100.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 7,
        'name': 'Super чистка лица',
        'description': 'Чистка лица с использованием Super методов для удаления загрязнений и улучшения текстуры кожи.',
        'price': 120.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 8,
        'name': 'Комбинированная чистка зоны декольте',
        'description': 'Чистка зоны декольте с использованием комбинированных методов для удаления загрязнений и улучшения текстуры кожи.',
        'price': 80.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 9,
        'name': 'Ультразвуковая чистка верхней части спины',
        'description': 'Чистка верхней части спины с использованием ультразвуковых технологий для удаления загрязнений и улучшения текстуры кожи.',
        'price': 85.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 10,
        'name': 'Ультразвуковая чистка всей спины',
        'description': 'Чистка всей спины с использованием ультразвуковых технологий для удаления загрязнений и улучшения текстуры кожи.',
        'price': 100.00,
        'duration': 60,
        'category': 'Чистка'
    },
    {
        'id': 11,
        'name': 'Альгинатная маска',
        'description': 'Альгинатная маска для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 45.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 12,
        'name': 'Очищающая маска',
        'description': 'Очищающая маска для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 30.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 13,
        'name': 'Увлажняющая маска',
        'description': 'Увлажняющая маска для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 30.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 14,
        'name': 'Лифтинговая маска',
        'description': 'Лифтинговая маска для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 35.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 15,
        'name': 'Осветляющая маска',
        'description': 'Осветляющая маска для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 35.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 16,
        'name': 'Мультимаскинг маска',
        'description': 'Мультимаскинг маска для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 40.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 17,
        'name': 'Коллагеновый лист',
        'description': 'Коллагеновый лист для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 65.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 18,
        'name': 'Нейромаска Gaba Lift',
        'description': 'Нейромаска Gaba Lift для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 60.00,
        'duration': 60,
        'category': 'Маски для лица'
    },
    {
        'id': 19,
        'name': 'Моделирующий массаж',
        'description': 'Моделирующий массаж лица и рук с использованием специальных техник для улучшения контуров лица и рук.',
        'price': 65.00,
        'duration': 60,
        'category': 'Массаж лица и рук'
    },
    {
        'id': 20,
        'name': 'Пластический массаж',
        'description': 'Пластический массаж лица и рук с использованием специальных техник для улучшения контуров лица и рук.',
        'price': 60.00,
        'duration': 60,
        'category': 'Массаж лица и рук'
    },
    {
        'id': 21,
        'name': 'Массаж по Жаке',
        'description': 'Массаж лица и рук по методике Жаке с использованием специальных техник для улучшения контуров лица и рук.',
        'price': 45.00,
        'duration': 60,
        'category': 'Массаж лица и рук'
    },
    {
        'id': 22,
        'name': 'Массаж с сыворотками (аппаратный)',
        'description': 'Массаж лица и рук с использованием сывороток и аппаратных методов для улучшения контуров лица и рук.',
        'price': 60.00,
        'duration': 60,
        'category': 'Массаж лица и рук'
    },
    {
        'id': 23,
        'name': 'Массаж области вокруг глаз (аппаратный)',
        'description': 'Массаж области вокруг глаз с использованием аппаратных методов для улучшения контуров лица и рук.',
        'price': 25.00,
        'duration': 60,
        'category': 'Массаж лица и рук'
    },
    {
        'id': 24,
        'name': 'Массаж кистей рук + скрабирование',
        'description': 'Массаж кистей рук с использованием скрабирования для улучшения контуров лица и рук.',
        'price': 35.00,
        'duration': 60,
        'category': 'Массаж лица и рук'
    },
    {
        'id': 25,
        'name': 'Водородный пилинг',
        'description': 'Водородный пилинг для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 90.00,
        'duration': 60,
        'category': 'Пиллинги'
    },
    {
        'id': 26,
        'name': 'Кислородный пилинг',
        'description': 'Кислородный пилинг для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 90.00,
        'duration': 60,
        'category': 'Пиллинги'
    },
    {
        'id': 27,
        'name': 'Миндально-феруловый пилинг с лактобионовой кислотой',
        'description': 'Миндально-феруловый пилинг с лактобионовой кислотой для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 80.00,
        'duration': 60,
        'category': 'Пиллинги'
    },
    {
        'id': 28,
        'name': 'Азелаиновый пилинг',
        'description': 'Азелаиновый пилинг для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 90.00,
        'duration': 60,
        'category': 'Пиллинги'
    },
    {
        'id': 29,
        'name': 'Нейропилинг GABA&NANA',
        'description': 'Нейропилинг GABA&NANA для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 100.00,
        'duration': 60,
        'category': 'Пиллинги'
    },
    {
        'id': 30,
        'name': 'Лифтинговый комплекс',
        'description': 'Лифтинговый комплекс для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 90.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 31,
        'name': 'Лифтинговый тонус',
        'description': 'Лифтинговый тонус для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 120.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 32,
        'name': 'Увлажняющий комплекс',
        'description': 'Увлажняющий комплекс для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 80.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 33,
        'name': 'Осветляющий комплекс',
        'description': 'Осветляющий комплекс для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 60.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 34,
        'name': 'Противопигментный Lux',
        'description': 'Противопигментный Lux для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 110.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 35,
        'name': 'Антиоксидантный комплекс',
        'description': 'Антиоксидантный комплекс для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 60.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 36,
        'name': 'Противокуперозный комплекс',
        'description': 'Противокуперозный комплекс для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 60.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 37,
        'name': 'Периорбитальный комплекс',
        'description': 'Периорбитальный комплекс для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 30.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 38,
        'name': 'Комплекс \"Всё и сразу\"',
        'description': 'Комплекс \"Всё и сразу\" для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 200.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 39,
        'name': 'Комплекс Nana&Gaba (мегалифтинг)',
        'description': 'Комплекс Nana&Gaba (мегалифтинг) для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.   ',
        'price': 150.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 40,
        'name': '',
        'description': '',
        'price': 100.00,
        'duration': 60,
        'category': 'Уходовые комплексы'
    },
    {
        'id': 41,
        'name': 'Дарсонваль лицо',
        'description': 'Дарсонваль для лица с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 15.00,
        'duration': 60,
        'category': 'Дарсонваль'
    },
    {
        'id': 42,
        'name': 'Дарсонваль волосы',
        'description': 'Дарсонваль для волос с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 25.00,
        'duration': 60,
        'category': 'Дарсонваль'
    },
    {
        'id': 43,
        'name': 'Дарсонваль спина',
        'description': 'Дарсонваль для спины с увлажняющим и питательным эффектом. Подходит для всех типов кожи.',
        'price': 25.00,
        'duration': 60,
        'category': 'Дарсонваль'
    }
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
