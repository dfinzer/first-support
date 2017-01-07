from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask.ext.login import UserMixin


class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False,
                           server_default=db.func.now())

    def to_dict(self, keys=None):
        if keys is None:
            keys = [col.name for col in self.__table__.columns]
        return {col: getattr(self, col) for col in keys if getattr(self, col) is not None}


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=True, unique=True, index=True)
    password = db.Column(db.String(250))

    def __init__(self, email=None):
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if not self.password:
            return False
        return check_password_hash(self.password, password)