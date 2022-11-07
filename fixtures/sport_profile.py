import pytest

from models.choices import SportsEnum
from models.sports_profile import SportProfile, Sport


@pytest.fixture
def sport_profile(db):
    params = {
        "user_id": 4,
        "vo2_max": 10.4,
        "ftp": 25.3,
    }
    sport_profile = SportProfile(**params)
    sport = Sport(sport_name=SportsEnum.ATHLETICS.name)
    sport_profile.sports = [sport]
    db.session.add(sport_profile)
    db.session.commit()
    return sport_profile
