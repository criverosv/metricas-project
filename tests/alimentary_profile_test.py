import json

import pytest

from models.alimentary_profile import AlimentaryProfile
from models.choices import FeedingEnum, AllergyEnum, IntoleranceEnum


def test_create_alimentary_profile(test_client):
    params = {
        "user_id": 16,
        "allergies": ["LECHE_DE_VACA", "HUEVOS"],
        "intolerances": ["GLUTEN", "TRIGO"],
        "feeding": "VEGETARIANO"
    }
    response = test_client.post("profile/v1/alimentary", data=json.dumps(params), content_type='application/json')
    assert response.status_code == 201, "This should be the status code returned"
    alimentary_profile = AlimentaryProfile.query.filter(AlimentaryProfile.user_id == params["user_id"]).one_or_none()

    assert alimentary_profile.feeding.value == FeedingEnum.VEGETARIANO.value
    assert len(alimentary_profile.allergies) == 2
    allergies_alimentary_profile = [allergy.food_allergy.value for allergy in alimentary_profile.allergies]
    assert AllergyEnum.LECHE_DE_VACA.value in allergies_alimentary_profile
    assert AllergyEnum.HUEVOS.value in allergies_alimentary_profile
    assert len(alimentary_profile.intolerances) == 2
    intolerances_alimentary_profile = [intolerance.food_intolerance.value for intolerance in alimentary_profile.intolerances]
    assert IntoleranceEnum.GLUTEN.value in intolerances_alimentary_profile
    assert IntoleranceEnum.TRIGO.value in intolerances_alimentary_profile


def test_obtain_alimentary_profile(test_client, alimentary_profile):
    alimentary_profile = alimentary_profile()
    response = test_client.get(f"profile/v1/alimentary/{alimentary_profile.user_id}")
    assert response.status_code == 200, "Success response"
    assert response.json
    data = response.json
    assert data["user_id"] == alimentary_profile.user_id
    assert data["feeding"] == FeedingEnum.VEGETARIANO.value


def test_obtain_alimentary_profile_not_found(test_client):
    response = test_client.get(f"profile/v1/alimentary/{10000000}")
    assert response.status_code == 404
    assert response.json["msg"] == "No alimentary profile found for this user"


def test_update_alimentary_profile_not_found(test_client):
    params = {
        "user_id": 16,
        "allergies": ["LECHE_DE_VACA", "HUEVOS"],
        "intolerances": ["GLUTEN", "TRIGO"],
        "feeding": "VEGETARIANO"
    }
    response = test_client.put(f"profile/v1/alimentary/{10000000}", data=json.dumps(params),
                               content_type="application/json")
    assert response.status_code == 404
    assert response.json["msg"] == "No alimentary profile found for this user"


@pytest.mark.parametrize("intolerances", [["GLUTEN", "TRIGO"], []])
def test_update_alimentary_profile(test_client, alimentary_profile, intolerances):
    alimentary_profile = alimentary_profile()
    params = {
        "user_id": 16,
        "allergies": ["HUEVOS"],
        "intolerances": intolerances,
        "feeding": "VEGETARIANO"
    }
    response = test_client.put(f"profile/v1/alimentary/{alimentary_profile.user_id}", data=json.dumps(params),
                               content_type="application/json")
    assert response.status_code == 200
    assert response.json
    data = response.json
    assert data["user_id"] == params["user_id"]

    alimentary_profile = AlimentaryProfile.query.filter(AlimentaryProfile.user_id == params["user_id"]).one_or_none()
    assert alimentary_profile.user_id == params["user_id"]
    allergies = [allergy.food_allergy.value for allergy in alimentary_profile.allergies]
    assert "HUEVOS" in allergies
    intolerances = [intolerance.food_intolerance.value for intolerance in alimentary_profile.intolerances]
    if intolerances:
        assert "GLUTEN" in intolerances
        assert "TRIGO" in intolerances
    else:
        assert len(intolerances) == 0


def test_obtain_alimentary_profile_not_allergies_not_intolerance(test_client, alimentary_profile):
    alimentary_profile = alimentary_profile(food_allergies=[], food_intolerances=[])
    response = test_client.get(f"profile/v1/alimentary/{alimentary_profile.user_id}")
    assert response.status_code == 200, "Success response"
    assert response.json
    data = response.json
    assert data["user_id"] == alimentary_profile.user_id
    assert data["feeding"] == FeedingEnum.VEGETARIANO.value


def test_alimentary_params_allergies(test_client):
    response = test_client.get("profile/v1/alimentary-params?param=allergies")
    assert response.status_code == 200
    assert response.json
    data = response.json
    params_to_compare = {
        AllergyEnum.HUEVOS.name: AllergyEnum.HUEVOS.value,
        AllergyEnum.LECHE_DE_VACA.name: AllergyEnum.LECHE_DE_VACA.value,
        AllergyEnum.PESCADO_O_MARISCOS.name: AllergyEnum.PESCADO_O_MARISCOS.value,
        AllergyEnum.FRUTOS_SECOS.name: AllergyEnum.FRUTOS_SECOS.value,
        AllergyEnum.TRIGO.name: AllergyEnum.TRIGO.value,
        AllergyEnum.FRUTAS.name: AllergyEnum.FRUTAS.value,
        AllergyEnum.VERDURAS.name: AllergyEnum.VERDURAS.value,
        AllergyEnum.SOJA.name: AllergyEnum.SOJA.value,
    }
    assert data == params_to_compare


def test_alimentary_params_intolerance(test_client):
    response = test_client.get("profile/v1/alimentary-params?param=intolerances")
    assert response.status_code == 200
    assert response.json
    data = response.json
    params_to_compare = {
        IntoleranceEnum.LACTOSA.name: IntoleranceEnum.LACTOSA.value,
        IntoleranceEnum.GLUTEN.name: IntoleranceEnum.GLUTEN.value,
        IntoleranceEnum.SACAROSA.name: IntoleranceEnum.SACAROSA.value,
        IntoleranceEnum.FRUCTOSA.name: IntoleranceEnum.FRUCTOSA.value,
        IntoleranceEnum.HISTAMINA.name: IntoleranceEnum.HISTAMINA.value,
        IntoleranceEnum.TRIGO.name: IntoleranceEnum.TRIGO.value,
    }
    assert data == params_to_compare


def test_alimentary_params_feeding(test_client):
    response = test_client.get("profile/v1/alimentary-params?param=feeding")
    assert response.status_code == 200
    assert response.json
    data = response.json
    params_to_compare = {
        FeedingEnum.VEGETARIANO.name: FeedingEnum.VEGETARIANO.value,
        FeedingEnum.OMNIVORO.name: FeedingEnum.OMNIVORO.value,
    }
    assert data == params_to_compare


def test_alimentary_params_another_param(test_client):
    response = test_client.get("profile/v1/alimentary-params?param=another-param")
    assert response.status_code == 404
    assert response.json["msg"] == "Either allergies, intolerances, or feeding param required"


def test_alimentary_params_no_param(test_client):
    response = test_client.get("profile/v1/alimentary-params")
    assert response.status_code == 400
    assert response.json
    assert response.json["msg"] == "Error. This endpoint must receive an argument called param"
