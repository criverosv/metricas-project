import json

import pytest

from models.choices import SportsEnum, InjuryEnum, ATHLETICS_INJURIES, CYCLING_INJURIES
from models.sports_profile import SportProfile


def test_obtain_sport_profile_success(test_client, sport_profile):
    response = test_client.get(f"profile/v1/sport/{sport_profile.user_id}", content_type="application/json")
    assert response.status_code == 200
    assert response.json
    data = response.json
    assert data["user_id"] == sport_profile.user_id
    assert data["ftp"] == sport_profile.ftp
    assert data["vo2_max"] == sport_profile.vo2_max
    assert data["sports"]
    assert "ATLETISMO" in data["sports"]


def test_obtain_sport_profile_not_found(test_client):
    response = test_client.get("profile/v1/sport/10000000", content_type="application/json")
    assert response.status_code == 404
    assert response.json["msg"] == "No sport profile found for this user"


def test_create_sport_profile(test_client):
    params = {
        "user_id": 4,
        "vo2_max": 10.4,
        "ftp": 25.3,
        "sports": [SportsEnum.ATHLETICS.value],
        "injuries": [InjuryEnum.ROTULA.value, InjuryEnum.TENDINITIS.value],
        "hours_of_practice_by_week": 5
    }
    response = test_client.post("profile/v1/sport", data=json.dumps(params), content_type="application/json")
    assert response.status_code == 201
    assert response.json
    data = response.json

    sport_profile = SportProfile.query.filter(SportProfile.user_id == params["user_id"]).one_or_none()
    assert sport_profile
    assert data["user_id"] == sport_profile.user_id
    assert data["vo2_max"] == sport_profile.vo2_max
    assert data["ftp"] == sport_profile.ftp
    assert data["hours_of_practice_by_week"] == sport_profile.hours_of_practice_by_week
    assert "ATLETISMO" in data["sports"]
    assert "ATLETISMO" in [sport.sport_name.value for sport in sport_profile.sports]
    injuries = [injury.injury_name.value for injury in sport_profile.injuries]
    assert "ROTULA" in injuries
    assert "TENDINITIS" in injuries


@pytest.mark.parametrize("update_sports", (True, False))
def test_update_sport_profile_success(test_client, sport_profile, update_sports):
    params = {
        "ftp": 28,
        "hours_of_practice_by_week": 10
    }
    if update_sports:
        params.update({"sports": [SportsEnum.CYCLING.value]})
    else:
        params.update({"sports": [SportsEnum.ATHLETICS.value]})

    response = test_client.put(f"profile/v1/sport/{sport_profile.user_id}", data=json.dumps(params),
                               content_type="application/json")
    assert response.status_code == 200
    assert response.json
    data = response.json
    assert data["ftp"] == params["ftp"]
    assert data["hours_of_practice_by_week"] == params["hours_of_practice_by_week"]
    assert data["vo2_max"] == sport_profile.vo2_max, "As this value was not updated, it should be the same"

    if update_sports:
        assert "ATLETISMO" not in data["sports"], "As it was not selected, it should be removed from the sports for this user"
        assert "ATLETISMO" not in [sport.sport_name.value for sport in sport_profile.sports]
        assert "CICLISMO" in data["sports"]
    else:
        assert "ATLETISMO" in data["sports"], "As it was selected, it should be on the list of sports"
        assert "ATLETISMO" in [sport.sport_name.value for sport in sport_profile.sports]
        assert "CICLISMO" not in data["sports"]


def test_update_sport_profile_not_found(test_client):
    params = {
        "ftp": 28,
        "sport": SportsEnum.CYCLING.value
    }
    response = test_client.put("profile/v1/sport/10000000", data=json.dumps(params),
                               content_type="application/json")
    assert response.status_code == 404
    assert response.json["msg"] == "No sport profile found for this user"


def test_get_sports_param(test_client):
    response = test_client.get("profile/v1/sport-params?param=sports", content_type="application/json")
    assert response.status_code == 200
    assert response.json == {
        "CYCLING": "CICLISMO",
        "ATHLETICS": "ATLETISMO"
    }


def test_get_sports_wrong_param(test_client):
    response = test_client.get("profile/v1/sport-params?param=wrong-param", content_type="application/json")
    assert response.status_code == 404
    assert response.json["msg"] == "Error. Wrong param"


@pytest.mark.parametrize("sport_name", ["ciclismo", "atletismo"])
def test_get_injuries_by_sport(test_client, sport_name):
    response = test_client.get(f"profile/v1/injuries?sport={sport_name}", content_type="application/json")
    assert response.status_code == 200
    assert response.json
    data = response.json
    assert isinstance(data, dict)
    if sport_name == "ciclismo":
        assert data == CYCLING_INJURIES
    elif sport_name == "atletismo":
        assert data == ATHLETICS_INJURIES
