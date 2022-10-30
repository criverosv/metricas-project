import pytest

from microservices.profile.models.alimentary_profile import AlimentaryProfile, Allergy, Intolerance
from microservices.profile.models.choices import AllergyEnum, IntoleranceEnum, FeedingEnum


@pytest.fixture
def alimentary_profile(db):
    def wrapper(food_allergies=[AllergyEnum.LECHE_DE_VACA.name, AllergyEnum.HUEVOS.name],
                food_intolerances=[IntoleranceEnum.GLUTEN.name, IntoleranceEnum.TRIGO.name]):
        params = {
            "user_id": 16,
        }
        alimentary_profile = AlimentaryProfile(**params)
        db.session.add(alimentary_profile)
        db.session.commit()
        allergies = []
        for food_allergy in food_allergies:
            allergies.append(Allergy(food_allergy=food_allergy, alimentary_profile_id=alimentary_profile.id))
        alimentary_profile.allergies = allergies
        intolerances = []
        for food_intolerance in food_intolerances:
            intolerances.append(Intolerance(food_intolerance=food_intolerance, alimentary_profile_id=alimentary_profile.id))
        alimentary_profile.intolerances = intolerances
        alimentary_profile.feeding = FeedingEnum.VEGETARIANO
        db.session.commit()
        return alimentary_profile
    return wrapper
