from flask import render_template, flash, redirect, request  # подключение функции для генерации веб-страниц,
# flash - функция для показа уведомлений пользователю,redirect - функция для перенаправления на другую страницу
from app import app, db  # подключение веб-приложения и базы данных
from app.forms import LoginForm, RegForm, TaskForm  # подключение формы для входа, регистрации и добавления задач
from flask_login import current_user, login_user, logout_user, login_required # подключение current_user(пользователь, находящийся на сайте),
# login_user(пользовательский загрузчик),logout_user(функция для выхода из системы), login_required(создание страниц,
# защищённых от просмотра не вошедшими пользователями
from app.models import User, Task, solved_tasks # подключение модели пользователей из базы данных



@app.route('/')  # создание главного маршрута
@app.route('/main')  # создание второго главного маршрута
@login_required
def main():  # функция обработчик
    #user = {'username': 'Анна'}  # создание фиктивного пользовалеля
    tasks = current_user.not_solved_tasks() # загрузка всех задач из базы данных
    return render_template('main.html', title='Главная', tasks=tasks, solved_tasks=solved_tasks)  # генерация страницы по шаблону main.html


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


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks = user.solved_tasks()
    return render_template('user.html', user=user, tasks=tasks, solved_tasks=solved_tasks)

@app.route('/admin', methods=['GET', 'POST'])  # маршрут панели админа;метод get-показ информации пользователю, метод post-отправка данных на сервер)
@login_required
def admin(): # функция обработчик маршрута
    if not current_user.admin:# если текущий пользователь не админ
        flash('Для доступа нужны права администратора')# сообщение для пользователя
        return redirect('/main') # перенаправление на главную
    form = TaskForm() # создание экземпляра формы
    if form.validate_on_submit(): # если пользователь нажмёт кнопку добавить, то
        task = Task(
            body=form.body.data,
            link=form.link.data,
            answer=form.answer.data,
            author=form.author.data
        ) # добавление задачи в базу данных
        db.session.add(task)
        db.session.commit() #сохранение изменений в базе данных
        flash('Задача успешно добавлена') # сообщение админу
        return redirect('/admin') # перенаправление на эту же страницу
    return render_template('admin.html', form=form) # генерация страницы по шаблону admin.html

@app.route('/result/<id>')
@login_required
def result(id):
    task = Task.query.get(int(id))
    if request.args.get('answer') == task.answer:
        current_user.count_correct_tasks += 1
        flash('Задача решена верно')
    else:
        flash('Задача решена неверно')
    current_user.count_tasks += 1
    current_user.tasks.append(task)
    db.session.commit()
    solved_tasks.update().where(solved_tasks.c.user_id==current_user.id, solved_tasks.c.task_id==task.id).values(answer=request.args.get('answer'))
    db.session.commit()
    return redirect(f'/main#{id}')
