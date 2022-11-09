from flask import request
from flask_restful import Resource

from models import db
from models.alimentary_profile import AlimentaryProfile, Allergy, Intolerance, alimentary_profile_schema
from models.choices import AllergyEnum, IntoleranceEnum, FeedingEnum
from sqlalchemy.exc import IntegrityError


class AlimentaryResource(Resource):

    schema = alimentary_profile_schema

    def get(self, user_id):
        alimentary_profile = AlimentaryProfile.query.filter(AlimentaryProfile.user_id == user_id).one_or_none()
        if alimentary_profile:
            allergies = alimentary_profile.allergies
            intolerances = alimentary_profile.intolerances
            to_return = self.schema.dump(alimentary_profile)
            if allergies:
                allergies_profile = [allergy.food_allergy.value for allergy in allergies]
                to_return["allergies"] = allergies_profile
            if intolerances:
                intolerances_profile = [intolerance.food_intolerance.value for intolerance in intolerances]
                to_return["intolerances"] = intolerances_profile
            return to_return, 200
        return AlimentaryResource.error_not_found()

    def post(self):
        params = request.json
        allergies = params.get("allergies", [])
        intolerances = params.get("intolerances", [])
        feeding = params.get("feeding")
        alimentary_profile = AlimentaryProfile(user_id=params["user_id"], feeding=feeding)
        try:
            db.session.add(alimentary_profile)
            db.session.commit()
            for allergy in allergies:
                allergy_obj = Allergy(alimentary_profile_id=alimentary_profile.id, food_allergy=allergy)
                db.session.add(allergy_obj)
            for intolerance in intolerances:
                intolerance_obj = Intolerance(alimentary_profile_id=alimentary_profile.id, food_intolerance=intolerance)
                db.session.add(intolerance_obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"msg": "Error while saving the alimentary profile"}
        return self.schema.dump(alimentary_profile), 201

    def put(self, user_id):
        params = request.json
        allergies_selected = params.get("allergies", [])
        intolerances_selected = params.get("intolerances", [])
        alimentary_profile = AlimentaryProfile.query.filter(AlimentaryProfile.user_id == user_id).one_or_none()
        if alimentary_profile:
            allergies_already_in_profile = alimentary_profile.allergies
            intolerances_already_in_profile = alimentary_profile.intolerances
            for allergy in allergies_already_in_profile:
                if allergy.food_allergy.name not in allergies_selected:
                    db.session.delete(allergy)
            for intolerance in intolerances_already_in_profile:
                if intolerance.food_intolerance.name not in intolerances_selected:
                    db.session.delete(intolerance)
            db.session.commit()
            return self.schema.dump(alimentary_profile), 200
        else:
            return AlimentaryResource.error_not_found()

    @staticmethod
    def error_not_found():
        return {"msg": "No alimentary profile found for this user"}, 404


class AlimentaryParams(Resource):

    def get(self):
        args = request.args
        try:
            param_to_return = args["param"]
            if param_to_return == "allergies":
                return {allergy.name: allergy.value for allergy in AllergyEnum}, 200
            elif param_to_return == "intolerances":
                return{intolerance.name: intolerance.value for intolerance in IntoleranceEnum}, 200
            elif param_to_return == "feeding":
                return {feeding.name: feeding.value for feeding in FeedingEnum}, 200
            else:
                return {"msg": "Either allergies, intolerances, or feeding param required"}, 404
        except KeyError:
            return {"msg": "Error. This endpoint must receive an argument called param"}, 400
