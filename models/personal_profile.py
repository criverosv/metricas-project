from marshmallow import Schema, fields
from sqlalchemy import Enum, UniqueConstraint

from . import db
from choices import GenreEnum, IdTypeEnum


class PersonalProfile(db.Model):
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_id_personal'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    id_type = db.Column(Enum(IdTypeEnum))
    id_number = db.Column(db.Integer)
    genre = db.Column(Enum(GenreEnum))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)


class PersonalProfileSchema(Schema):
    name = fields.Str()
    last_name = fields.Str()
    id_type = fields.Enum(IdTypeEnum, by_value=True)
    id_number = fields.Integer()
    genre = fields.Enum(GenreEnum, by_value=True)
    age = fields.Integer()
    weight = fields.Integer()
    height = fields.Integer()
    user_id = fields.Integer()


personal_schema = PersonalProfileSchema()
