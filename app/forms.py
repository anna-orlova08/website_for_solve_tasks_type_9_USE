from flask_wtf import FlaskForm  # подключение шаблона для создания собственных форм
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    SubmitField  # подключение полей для ввода строк и паролей, расстановки галочек, кнопки входа
from wtforms.validators import DataRequired  # подключение валидатора для проверки пустого поля
from wtforms.validators import ValidationError, Email, EqualTo, URL  # ValidationError-создание собственного валидатора,
# Email-проверка соответствия почты установленным правилам, EqualTo- проверка совпадения полей формы
from app.models import User  # подключение модели пользователей из базы данных


class LoginForm(FlaskForm):  # создание формы для входа
    username = StringField('Имя пользователя', validators=[DataRequired()])  # создание поля для ввода имени пользователя
    password = PasswordField('Пароль', validators=[DataRequired()])  # создание поля для ввода пароля
    remember_me = BooleanField('Запомнить меня')  # галочка  запомнить меня
    submit = SubmitField('Войти')  # кнопка для входа


class RegForm(FlaskForm):  # создание формы для регистрации
    username = StringField('Имя пользователя', validators=[DataRequired()])  # создание поля для ввода имени пользователя
    email = StringField('Email',validators=[DataRequired(), Email()]) # создание поля для ввода email
    password = PasswordField('Пароль', validators=[DataRequired()])  # создание поля для ввода пароля
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])  # создание поля для проверки пароля
    submit = SubmitField('Зарегистрироваться')  # кнопка для регистрации

    def validate_username(self, username): # создание валидатора для проверки, что такого имени пользователя нет в базе данных
        user = User.query.filter_by(username=username.data).first() # поиск пользователя в базе данных по указанному имени
        if user is not None: # если пользователя удалось найти
            raise ValidationError('Имя пользователя занято') # возврат ошибки пользователю

    def validate_email(self, email): # создание валидатора для проверки, что такой почты нет в базе данных
        user = User.query.filter_by(email=email.data).first()  # поиск пользователя в базе данных по указанной почте
        if user is not None:  # если пользователя удалось найти
            raise ValidationError('Пользователь с такой почтой зарегистрирован') # возврат ошибки пользователю


class TaskForm(FlaskForm):  # создание формы для добавления задач
    body = TextAreaField('Текст задачи', validators=[DataRequired()]) # поле для текста задач
    link = StringField('Ссылка на файл', validators=[DataRequired(), URL()]) # поле для ссылки на файл
    answer = StringField('Правильный ответ', validators=[DataRequired()]) # поле для правильного ответа к задаче
    author = StringField('Источник', validators=[DataRequired()]) # поле для ввода источника задачи
    submit = SubmitField('Добавить задачу')

    def validate_answer(self,answer): # проверка, что число в ответе целое
        if not answer.data.isdigit(): # проверка,что в строке только цифры
            raise ValidationError('В ответе должны быть только цифры') # возврат ошибки пользователю

