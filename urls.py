from flask_restful import Api

from views.personal_profile import PersonalResource
from views.alimentary_profile import AlimentaryResource, AlimentaryParams
from views.demographic_profile import DemographicParams, DemographicResource
from views.health_check import HealthCheck
from views.sport_profile import SportResource


def register_routes(app):
    api = Api(app, '/profile/')

    api.add_resource(HealthCheck, '')
    api.add_resource(PersonalResource, 'v1/personal', 'v1/personal/<int:user_id>')
    api.add_resource(AlimentaryResource, 'v1/alimentary', 'v1/alimentary/<int:user_id>')
    api.add_resource(AlimentaryParams, 'v1/alimentary-params')
    api.add_resource(DemographicParams, 'v1/demographic-params/countries')
    api.add_resource(DemographicResource, 'v1/demographic', 'v1/demographic/<int:user_id>')
    api.add_resource(SportResource, 'v1/sport', 'v1/sport/<int:user_id>')
