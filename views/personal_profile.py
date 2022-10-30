from flask import request
from flask_restful import Resource

from models import db
from models.personal_profile import personal_schema, PersonalProfile


class PersonalResource(Resource):
    schema = personal_schema

    def post(self):
        validated_data = self.schema.load(request.json)
        personal_info = PersonalProfile(**validated_data)
        db.session.add(personal_info)
        db.session.commit()
        return self.schema.dump(personal_info), 201

    def get(self, user_id):
        personal_info = PersonalProfile.query.filter(PersonalProfile.user_id == user_id).one_or_none()
        if personal_info:
            return self.schema.dump(personal_info), 200
        return PersonalResource.error_not_found()

    def put(self, user_id):
        validated_data = self.schema.load(request.json, partial=True)
        personal_info = PersonalProfile.query.filter(PersonalProfile.user_id == user_id).one_or_none()
        if personal_info:
            for name, value in validated_data.items():
                setattr(personal_info, name, value)
            db.session.commit()
            return self.schema.dump(personal_info), 200
        return PersonalResource.error_not_found()

    @staticmethod
    def error_not_found():
        return {"msg": "Not personal profile found for the id provided"}, 404
