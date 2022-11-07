from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models import db
from models.demographic_profile import demographic_profile_schema, DemographicProfile
from utils.countries_cities import get_all_countries, get_all_cities_from_country


class DemographicParams(Resource):

    def get(self):
        args = request.args
        if args:
            country = args.get("country")
            if country:
                return get_all_cities_from_country(country), 200
            return {"msg": "Error, wrong param"}, 404
        return get_all_countries(), 200


class DemographicResource(Resource):

    schema = demographic_profile_schema

    def get(self, user_id):
        demographic_profile = DemographicProfile.query.filter(DemographicProfile.user_id == user_id).one_or_none()
        if demographic_profile:
            return self.schema.dump(demographic_profile), 200
        return DemographicResource.error_not_found()

    def post(self):
        try:
            validated_data = self.schema.load(request.json)
            demographic_profile = DemographicProfile(**validated_data)
            db.session.add(demographic_profile)
            db.session.commit()
            return self.schema.dump(demographic_profile), 201
        except Exception as ex:
            db.session.rollback()
            return {"msg": "Error creating the demographic profile"}, 400
        except ValidationError as err:
            return {"msg": f"Error validating data {err.messages}"}

    def put(self, user_id):
        request.json.pop("user_id")
        validated_data = self.schema.load(request.json, partial=True)
        demographic_profile = DemographicProfile.query.filter(DemographicProfile.user_id == user_id).one_or_none()
        if demographic_profile:
            for attr, value in validated_data.items():
                setattr(demographic_profile, attr, value)
            db.session.commit()
            return self.schema.dump(demographic_profile), 200
        else:
            return DemographicResource.error_not_found()

    @staticmethod
    def error_not_found():
        return {"msg": "No demographic profile found for this user"}, 404
