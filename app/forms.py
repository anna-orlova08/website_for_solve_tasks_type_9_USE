from flask_wtf import FlaskForm  # подключение шаблона для создания собственных форм
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField  # подключение полей для ввода строк и паролей,расстановки галочек,кпопки входа
from wtforms.validators import DataRequired  # подключение валидатора для проверки пустого поля


class LoginForm(FlaskForm):  # создание формы для входа
    username = StringField('Имя пользователя',
                           validators=[DataRequired()])  # создание поля для ввода  имени пользователя
    password = PasswordField('Пароль', validators=[DataRequired()])  # создание поля  для ввода пароля
    remember_me = BooleanField('Запомнить меня')  # галочка  запомнить меня
    submit = SubmitField('Войти')  # кнопка для входа
