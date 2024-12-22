from app import app,db #подключение веб-приложения и базы данных
from app.models import User, Task # импорт таблиц пользователей и задач

@app.shell_context_processor # создание контекста оболочки
def make_shell_context(): # функция, которая запускается при вызове контекста оболочки
    return {'db': db,'User':User,'Task':Task} # функция возвращает словарь с базой данных и таблицами пользователей и задач


