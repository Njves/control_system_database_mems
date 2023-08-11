import uuid
from datetime import datetime
from time import time

import jwt
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask import current_app as app
from flask_login import UserMixin
from app.search import add_to_index, remove_from_index, query_index

@login.user_loader
def load_user(id):
    return Account.query.get(int(id))


mem_tag = db.Table('MemTag',
                   db.Column('mem_id', db.Integer, db.ForeignKey('mem.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                   comment='Auxiliary table of meme and tag connection')

roles_account = db.Table(
    'AccountRole',
    db.Column('account_id', db.Integer(), db.ForeignKey('account.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class SearchableMixin(object):
    @classmethod
    def search(cls, expression):
        ids, total = query_index(cls.__tablename__, expression)
        print(total)
        if total['value'] == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Message: {self.body} sender {self.sender_id} recipient {self.recipient_id}'


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='date of registation')
    avatar = db.Column(db.String(128), default='icon/avatar_placeholder.png', comment='link to avatar')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='last seen user in online')
    uid = db.Column(db.String(128), nullable=False, default=str(uuid.uuid4()), comment="unique user id")
    mems = db.relationship('Mem', backref='owner', lazy='dynamic')
    roles = db.relationship('Role', secondary=roles_account,
                            backref=db.backref('accounts', lazy='dynamic'))

    __searchable__ = ['username']

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    @property
    def amount(self):
        return self.mems.count()

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.id == other.id and self.username == other.username and self.email == other.email and \
                self.date == other.date and self.avatar == other.avatar and self.amount == other.amount and \
                self.uid == other.uid
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            account = Account.query.get(jwt.decode(token, app.config['SECRET_KEY'],
                                                   algorithms=['HS256'])['reset_password'])
            print(account)
            return account
        except jwt.InvalidTokenError:
            # TODO: Добавить логирование
            return
    def __repr__(self):
        return f"Account: ('username': {self.username})," \
               f" ('date': {self.date})," \
               f" ('picture': {self.avatar})," \
               f" ('amount': {self.amount}),"


class Mem(SearchableMixin, db.Model):

    __searchable__ = ['name', 'description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    link = db.Column(db.String(128), nullable=False, comment='Path mem image')
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='Date the meme was created')
    description = db.Column(db.String(128), comment='Mem description')
    likes = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, nullable=False, default=0, comment='Access level, 0 - private, 1 - public')
    uid = db.Column(db.String(128), comment='unique id mem')
    view = db.Column(db.Integer, default=0, comment="Number of views")
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    tags = db.relationship('Tag', secondary=mem_tag, backref=db.backref('mems'))



    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.link == other.link and self.date == other.date and \
            self.description == other.description and self.likes == other.likes and self.status == other.status and self.uid == other.uid and \
            self.owner_id == other.owner_id and self.tags == other.tags

    def __repr__(self):
        return f"Mem: ('id': {self.id})," \
               f" ('name': {self.name})," \
               f" ('link': {self.link})," \
               f" ('date': {self.date})," \
               f" ('description': {self.description})," \
               f" ('likes': {self.likes})," \
               f" ('status': {self.status}," \
               f" ('uid': {self.uid})," \
               f" ('tags': {self.tags})," \
               f" ('owner_id': {self.owner_id}"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    uid = db.Column(db.String(128), comment='unique id')

    __searchable__ = ['name']

    def __repr__(self):
        return f"Tag: ('id': {self.id})," \
               f" ('name': {self.name})," \
               f" ('date': {self.date})," \
               f" ('uid': {self.uid}),"





class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

