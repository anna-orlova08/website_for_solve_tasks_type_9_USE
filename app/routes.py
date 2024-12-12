from flask import render_template, flash, redirect  # подключение функции для генерации веб-страниц,
# flash - функция для показа уведомлений пользователю,redirect - функция для перенаправления на другую страницу
from app import app  # подключение веб-приложения
from app.forms import LoginForm  # подключение формы для входа


@app.route('/')  # создание главного маршрута
@app.route('/main')  # создание второго главного маршрута
def main():  # функция обработчик
    user = {'username': 'Анна'}  # создание фиктивного пользовалеля
    tasks = [  # создание списка задач с авторами
        {
            'author': {'username': 'Дарья'},  # фиктивный пользователь автор
            'body': 'задача 1'  # текст будущей задачи
        },
        {
            'author': {'username': 'Варвара'},
            'body': 'задача 2'
        },
        {
            'author': {'username': 'Анна'},
            'body': 'задача 3'
        }
    ]
    return render_template('main.html', title='Главная', user=user,
                           tasks=tasks)  # генерация страницы по шаблону main.html


@app.route('/login', methods=['GET',
                              'POST'])  # маршрут страницы входа;метод get-показ информации пользователю, метод post-отправка данных на сервер
def login():  # функция обработчик маршрута
    form = LoginForm()  # создание экземпляра формы входа
    if form.validate_on_submit():  # если пользователь нажмёт на кнопку входа,то
        flash(f'Привет, {form.username.data}!')  # показ уведомления пользователю об успешном входе
        return redirect('/main')  # перенаправление на главную страницу
    return render_template('login.html', title='Вход', form=form)  # генерация страницы по шаблону login.html
