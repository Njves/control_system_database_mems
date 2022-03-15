from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Account.query.get(int(id))


# status: 0 - private, 1 - public
class Mem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Название мема
    name = db.Column(db.String(128))
    # Ссылка на картинку
    link = db.Column(db.String(128), nullable=False)
    # Дата загрузки мема
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # Описание мема
    description = db.Column(db.String(128), nullable=False)
    # Кол-во лайки
    likes = db.Column(db.Integer)
    # Видимость мема публичная/приватная
    status = db.Column(db.Integer, nullable=False, default=0)
    # уникальный id
    uid = db.Column(db.String(128))
    # id загрузчика
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f"Mem: ('id': {self.id})," \
               f" ('name': {self.name})," \
               f" ('link': {self.link})," \
               f" ('date': {self.date})," \
               f" ('description': {self.description})," \
               f" ('likes': {self.likes})," \
               f" ('status': {self.status}," \
               f" ('uid': {self.uid})," \
               f" ('owner_id': {self.owner_id}"


# Одна единица тега
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # название
    name = db.Column(db.String(64))
    # дата создания тега
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # уникальный id тега
    uid = db.Column(db.String(128))


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # имя пользователя
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # ссылка на картинку
    picture = db.Column(db.String(128))
    # загруженных картинок
    amount = db.Column(db.Integer, default=0)
    # список картинок пользователя
    mems = db.relationship('Mem', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Account: ('username': {self.username})," \
               f" ('password': {self.password})," \
               f" ('date': {self.date})," \
               f" ('picture': {self.picture})," \
               f" ('amount': {self.amount}),"


MemTag = db.Table('MemTag',
                  db.Column('mem_id', db.Integer, db.ForeignKey('mem.id')),
                  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
