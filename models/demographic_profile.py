from marshmallow import Schema, fields
from sqlalchemy import UniqueConstraint

from . import db


class DemographicProfile(db.Model):
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_id_demographic'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    birth_country = db.Column(db.String(30))
    birth_city = db.Column(db.String(30))
    residence_country = db.Column(db.String(30))
    residence_city = db.Column(db.String(30))
    residence_seniority = db.Column(db.Integer)


class DemographicProfileSchema(Schema):
    birth_country = fields.Str(allow_none=False)
    birth_city = fields.Str(allow_none=False)
    residence_country = fields.Str(allow_none=False)
    residence_city = fields.Str(allow_none=False)
    residence_seniority = fields.Integer(allow_none=False)
    user_id = fields.Integer(allow_none=False)


demographic_profile_schema = DemographicProfileSchema()
