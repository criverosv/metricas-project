from marshmallow import Schema, fields
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from . import db
from .choices import SportsEnum


class SportProfile(db.Model):
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_id_sport'),)

    id = db.Column(db.Integer, primary_key=True)
    sports = relationship("Sport")
    ftp = db.Column(db.Float)
    vo2_max = db.Column(db.Float)
    user_id = db.Column(db.Integer)


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(Enum(SportsEnum))
    sport_profile_id = db.Column(db.Integer, db.ForeignKey("sport_profile.id"))


class SportSchema(Schema):
    sport_name = fields.Enum(SportsEnum, by_value=True)
    id = fields.Integer(dump_only=True)


class SportProfileSchema(Schema):
    sports = fields.List(fields.Pluck(SportSchema, 'sport_name'))
    ftp = fields.Float()
    vo2_max = fields.Float()
    user_id = fields.Integer()


sport_profile_schema = SportProfileSchema()
