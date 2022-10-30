from flask import request
from flask_restful import Resource

from models.sports_profile import SportProfile, sport_profile_schema, Sport

from models import db


class SportResource(Resource):
    schema = sport_profile_schema

    def get(self, user_id):
        sport_profile = SportProfile.query.filter(SportProfile.user_id == user_id).one_or_none()
        if sport_profile:
            return self.schema.dump(sport_profile), 200
        else:
            return SportResource.error_not_found()

    def post(self):
        validated_data = self.schema.load(request.json)
        try:
            sports = validated_data.pop("sports", [])
            sport_profile = SportProfile(**validated_data)
            db.session.add(sport_profile)
            db.session.commit()

            sports_to_add = []
            for sport in sports:
                sport = Sport(sport_name=sport["sport_name"].name)
                db.session.add(sport)
                sports_to_add.append(sport)

            sport_profile.sports = sports_to_add
            db.session.commit()
            return self.schema.dump(sport_profile), 201
        except Exception as ex:
            db.session.rollback()
            return {"msg": "There was an error saving the sport profile"}, 400

    def put(self, user_id):
        sport_profile = SportProfile.query.filter(SportProfile.user_id == user_id).one_or_none()
        if sport_profile:
            validated_data = self.schema.load(request.json)
            selected_sports = [sport["sport_name"].name for sport in validated_data.pop("sports", [])]

            for key, value in validated_data.items():
                setattr(sport_profile, key, value)
            sports_to_add = []
            try:
                for existent_sport in sport_profile.sports:
                    if existent_sport.sport_name.name not in selected_sports:
                        db.session.delete(existent_sport)
                db.session.commit()
                existent_sports = [sport.sport_name.name for sport in sport_profile.sports]
                for selected_sport in selected_sports:
                    if selected_sport not in existent_sports:
                        sport = Sport(sport_name=selected_sport)
                        db.session.add(sport)
                        sports_to_add.append(sport)
                if sports_to_add:
                    sport_profile.sports = sports_to_add
                    db.session.commit()
                return self.schema.dump(sport_profile), 200
            except Exception as ex:
                db.session.rollback()
                return {"msg": "Error updating the sport profile for this user"}, 400
        else:
            return SportResource.error_not_found()

    @staticmethod
    def error_not_found():
        return {"msg": "No sport profile found for this user"}, 404
