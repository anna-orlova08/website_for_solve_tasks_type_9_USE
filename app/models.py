from app import db, login  # импортирование базы данных и пользовательского загрузчика
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # подключение класса для отслеживания состояния пользователя
from hashlib import md5

solved_tasks = db.Table('solved tasks', # создание таблицы для связки пользователей и решённых ими задач
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')), # поле id пользователя
                        db.Column('task_id', db.Integer, db.ForeignKey('task.id')), # поле id задачи
                        db.Column('answer', db.Integer) # поле ответа пользователя
                        )

class Task(db.Model):# создание модели задач в базе данных
    id = db.Column(db.Integer, primary_key=True) # поле ID задач,db.Integer - целое число,primary_key-первичный ключ(уникален для всех задач)
    body = db.Column(db.String(1024)) # поле текста задачи, максимум 1024 символа
    link = db.Column(db.String(256)) # поле ссылки для скачивания файла
    answer = db.Column(db.String(32)) # поле правильного ответа к задаче
    author = db.Column(db.String(64)) # поле имени автора задачи
    link_solution = db.Column(db.String(256))


class User(UserMixin, db.Model): # создание модели пользователей в базе данных
    id = db.Column(db.Integer, primary_key=True) # поле ID пользователя,db.Integer - целое число, primary_key-первичный ключ(уникален для всех пользователей)
    username=db.Column(db.String(64), index=True, unique=True) # поле имени пользователя,db.String(64)-строка максимум 64 символа,index- упрощение поиска,uniqu-поле должно быть уникальным
    email=db.Column(db.String(120), index=True, unique=True) # поле почты пользователя
    password_hash=db.Column(db.String(128)) # поле хэша пароля(уникальный код, созданный по паролю; при входе сравнивается именно хэш)
    admin = db.Column(db.Boolean, default=False, nullable=False) # поле указания является ли пользователь админом, db.Boolean-логическое значение(либо true либо false),default=False-по умолчанию пользователь не админ,nullable=False-поле не может содержать нулевые значения
    count_tasks = db.Column(db.Integer, default=0 ) # поле количества решённых задач, значение по умолчанию 0
    count_correct_tasks = db.Column(db.Integer, default=0 ) # поле количества правильно решенных задач
    tasks = db.relationship( # поле связки
        'Task', secondary = solved_tasks, # указание таблицы, с которой идёт связка, и таблицы,в которой указано как связаны задачи и пользователи
        primaryjoin = (solved_tasks.c.user_id == id),
        secondaryjoin = (solved_tasks.c.task_id==Task.id),
        backref = db.backref('solvedtasks', lazy = 'dynamic'),# имя для связки и режим выполнения запроса
        lazy = 'dynamic'
    )
    def __repr__(self): # метод, который вызывается в случае вызова user без указания дополнительных действий
        return f'User <{self.username}>' # вывод имени вызванного пользователя

    def set_password(self,password): # метод для создания и изменения пароля
        self.password_hash = generate_password_hash(password) # создание хэша пароля для пользователя

    def check_password(self,password): # метод для проверки пароля
        return check_password_hash(self.password_hash,password) # вернёт true, если пароль правильный, или false, если пароль неправильный

    def avatar(self,size): # метод для демонстрации аватара
        digest = md5(self.email.lower().encode('utf-8')).hexdigest() # создание хеша по email пользователя в 16-ном коде
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}' # ссылка на аватар с сайта граватар, digest-хеш пользователя,d=identicon-картинка по умолчанию, s={size}-размер картинки

    def solved_tasks(self):
        return Task.query.join(
            solved_tasks, (solved_tasks.c.task_id==Task.id)).filter(
            solved_tasks.c.user_id==self.id)
    def not_solved_tasks(self):
        all_ = Task.query.filter()
        solved = self.solved_tasks()
        return all_.except_(solved)

    def task_is_solved(self, task):
        return self.tasks.filter(solved_tasks.c.task_id==task.id).count()>0



@login.user_loader # регистрирование пользовательского загрузчика
def load_user(id): # функция пользовательского загрузчика
    return User.query.get(int(id)) # возврат пользователя из базы данных по id



