from flask import Flask  # подключение Flask для создания веб-приложения(сайт)
from config import Config  # подключение инструкции для конфигурации
from flask_sqlalchemy import SQLAlchemy  # подключение библиотеки для работы с базой данных
from flask_migrate import Migrate  # подключение migrate для переноса данных при изменении структуры базы данных

app = Flask(__name__)  # создание веб-приложения
app.config.from_object(Config)  # конфигурации приложения
db = SQLAlchemy(app)  # создание экземпляра базы данных,связка с веб-приложением
migrate = Migrate(app, db)  # создание объекта для переноса данных при изменении структуры базы данных

from app import routes, models  # подключение маршрутов сайта
