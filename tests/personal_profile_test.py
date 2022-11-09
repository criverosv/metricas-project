import json
import random

from faker import Faker

from models.choices import MALE_ITEM, FEMALE_ITEM, \
    N_A_ITEM, IdTypeEnum
from models.personal_profile import PersonalProfile

fake = Faker()


def test_create_personal_profile(test_client):
    params = {
        "name": fake.name(),
        "last_name": fake.last_name(),
        "id_type": "CEDULA CIUDADANIA",
        "id_number": random.choice(range(100000, 1000000)),
        "genre": random.choice([MALE_ITEM, FEMALE_ITEM, N_A_ITEM]),
        "age": random.choice(range(10, 99)),
        "weight": random.choice(range(10, 99)),
        "height": random.choice(range(10, 99)),
        "user_id": random.choice(range(1, 1000000)),
    }

    APP_JSON = "application/json"
    response = test_client.post("profile/v1/personal", data=json.dumps(params), content_type=APP_JSON)
    assert response.status_code == 201, "This should be the status code returned after the profile has been created"

    personal_profile = PersonalProfile.query.filter(PersonalProfile.user_id==params["user_id"]).one_or_none()
    assert personal_profile
    assert personal_profile.name == params["name"]
    assert personal_profile.last_name == params["last_name"]
    assert personal_profile.id_type == IdTypeEnum.CEDULA_CIUDADANIA
    assert personal_profile.age == params["age"]


def test_update_personal_profile(test_client, personal_profile):
    params = {
        "weight": 60,
    }
    response = test_client.put(f"profile/v1/personal/{personal_profile.user_id}",
                               data=json.dumps(params),
                               content_type=APP_JSON)
    assert response.status_code == 200, "The update was success"
    assert response.json

    data = response.json
    assert data["weight"] == params["weight"], "The weight should be the new one"

    personal_profile = PersonalProfile.query.filter(PersonalProfile.id == personal_profile.id).one_or_none()
    assert personal_profile
    assert personal_profile.weight == params["weight"]


def test_obtain_personal_profile(test_client, personal_profile):
    response = test_client.get(f"profile/v1/personal/{personal_profile.user_id}", content_type=APP_JSON)
    assert response.status_code == 200
    assert response.json
    data = response.json

    assert data["name"] == personal_profile.name
    assert data["last_name"] == personal_profile.last_name
    assert data["id_type"] == "CEDULA CIUDADANIA"
    assert data["id_number"] == 12345678
    assert data["genre"] == "HOMBRE"
    assert data["age"] == 31
    assert data["weight"] == 54
    assert data["height"] == 168
    assert data["user_id"] == 10


def test_obtain_personal_profile_not_found(test_client):
    response = test_client.get(f"profile/v1/personal/{1000000000}", content_type=APP_JSON)
    assert response.status_code == 404
    assert response.json["msg"] == "Not personal profile found for the id provided"


def test_update_personal_profile_not_found(test_client):
    params = {
        "weight": 60,
    }
    response = test_client.put(f"profile/v1/personal/{1000000000}", data=json.dumps(params),
                               content_type=APP_JSON)
    assert response.status_code == 404
    assert response.json["msg"] == "Not personal profile found for the id provided"
