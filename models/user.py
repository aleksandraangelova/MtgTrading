from db import db
from models.enum import UserRole


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class TraderModel(BaseUserModel):
    __tablename__ = "trader"

    role = db.Column(db.Enum(UserRole), default=UserRole.trader, nullable=False)


class AdminModel(BaseUserModel):
    __tablename__ = "admin"
    role = db.Column(db.Enum(UserRole), default=UserRole.admin, nullable=False)
