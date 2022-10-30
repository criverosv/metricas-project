import pytest

from models.choices import IdTypeEnum, GenreEnum
from models.personal_profile import PersonalProfile


@pytest.fixture
def personal_profile(db):
    params = {
        "name": "name",
        "last_name": "last_name",
        "id_type": IdTypeEnum.CEDULA_CIUDADANIA,
        "id_number": 12345678,
        "genre": GenreEnum.MALE,
        "age": 31,
        "weight": 54,
        "height": 168,
        "user_id": 10,
    }
    personal_profile = PersonalProfile(**params)
    db.session.add(personal_profile)
    db.session.commit()
    return personal_profile
