from flask import render_template, flash, redirect  # подключение функции для генерации веб-страниц,
# flash - функция для показа уведомлений пользователю,redirect - функция для перенаправления на другую страницу
from app import app, db  # подключение веб-приложения и базы данных
from app.forms import LoginForm, RegForm  # подключение формы для входа и регистрации
from flask_login import current_user, login_user, logout_user, login_required # подключение current_user(пользователь, находящийся на сайте),
# login_user(пользовательский загрузчик),logout_user(функция для выхода из системы), login_required(создание страниц,
# защищённых от просмотра не вошедшими пользователями
from app.models import User # подключение модели пользователей из базы данных


@app.route('/')  # создание главного маршрута
@app.route('/main')  # создание второго главного маршрута
@login_required
def main():  # функция обработчик
    #user = {'username': 'Анна'}  # создание фиктивного пользовалеля
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
    return render_template('main.html', title='Главная', tasks=tasks)  # генерация страницы по шаблону main.html


@app.route('/login', methods=['GET',
                              'POST'])  # маршрут страницы входа;метод get-показ информации пользователю, метод post-отправка данных на сервер
def login():  # функция обработчик маршрута
    if current_user.is_authenticated: # если пользователь уже зашёл на сайт
        return redirect('/main') # перенаправление на главную страницу
    form = LoginForm()  # создание экземпляра формы входа
    if form.validate_on_submit():  # если пользователь нажмёт на кнопку входа,то
        user = User.query.filter_by(username=form.username.data).first() # поиск пользователя в базе данных по имени
        if user is None or not user.check_password(form.password.data): # если пользователь не найден или пароль введён неправильно
            flash('Имя пользователя или пароль неправильные') # показ уведомления пользователю о неправильных данных
            return redirect('/login') # перенаправление снова на страницу входа для повторной попытки
        login_user(user,remember=form.remember_me.data)
        #flash(f'Привет, {form.username.data}!')  # показ уведомления пользователю об успешном входе
        return redirect('/main')  # перенаправление на главную страницу
    return render_template('login.html', title='Вход', form=form)  # генерация страницы по шаблону login.html

@app.route('/logout') # маршрут страницы выхода
def logout(): # функция обработчик страницы
    logout_user() # выход пользователя из системы
    return redirect('/main') # перенаправление на главную страницу

@app.route('/register',methods=['GET',
                              'POST'])  # маршрут страницы регистрации;метод get-показ информации пользователю, метод post-отправка данных на сервер
def register():
    if current_user.is_authenticated: # если пользователь уже зашёл на сайт
        return redirect('/main') # перенаправление на главную страницу
    form = RegForm() # создание экземпляра формы регистрации
    if form.validate_on_submit():  # если пользователь нажмёт на кнопку регистрации, то
        user = User(username=form.username.data,email=form.email.data) # создание пользователя по введённым данным
        user.set_password(form.password.data) # изменение пароля пользователя
        db.session.add(user) # добавление пользователя в базу данных
        db.session.commit() # сохранение изменений в базе данных
        flash('Регистрация прошла успешно')
        return redirect('/login') # перенаправление на страницу входа
    return render_template('register.html',title='Регистрация',form=form) # генерация страницы по шаблону register.html
