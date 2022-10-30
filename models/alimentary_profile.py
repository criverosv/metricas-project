from marshmallow import Schema, fields
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from . import db
from .choices import AllergyEnum, IntoleranceEnum, FeedingEnum


class AlimentaryProfile(db.Model):
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_id_alimentary'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    feeding = db.Column(Enum(FeedingEnum))
    allergies = relationship("Allergy")
    intolerances = relationship("Intolerance")


class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_allergy = db.Column(Enum(AllergyEnum))
    alimentary_profile_id = db.Column(db.Integer, db.ForeignKey("alimentary_profile.id"))


class Intolerance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_intolerance = db.Column(Enum(IntoleranceEnum))
    alimentary_profile_id = db.Column(db.Integer, db.ForeignKey("alimentary_profile.id"))


class AllergySchema(Schema):
    food_allergy = fields.Enum(AllergyEnum, by_value=True)


class AlimentaryProfileSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    feeding = fields.Enum(FeedingEnum, by_value=True)


alimentary_profile_schema = AlimentaryProfileSchema()
