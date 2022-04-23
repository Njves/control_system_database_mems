from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Account.query.get(int(id))


mem_tag = db.Table('MemTag',
                   db.Column('mem_id', db.Integer, db.ForeignKey('mem.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                   comment='Auxiliary table of meme and tag connection')


class Mem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    link = db.Column(db.String(128), nullable=False, comment='Path mem image')
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='Date the meme was created')
    description = db.Column(db.String(128), comment='Mem description')
    likes = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, nullable=False, default=0, comment='Access level, 0 - private, 1 - public')
    uid = db.Column(db.String(128), comment='unique id mem')
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    tags = db.relationship('Tag', secondary=mem_tag, backref=db.backref('mems'))

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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    uid = db.Column(db.String(128), comment='unique id')


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, comment='date of registation')
    picture = db.Column(db.String(128), comment='link to avatar')
    amount = db.Column(db.Integer, default=0, comment='amount loaded mems')
    mems = db.relationship('Mem', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Account: ('username': {self.username})," \
               f" ('date': {self.date})," \
               f" ('picture': {self.picture})," \
               f" ('amount': {self.amount}),"
