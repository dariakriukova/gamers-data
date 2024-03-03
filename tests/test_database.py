from sqlalchemy.orm import Session
from database import Region
from database import upsert_region


class TestUpsertRegion:
    def test_upsert_new(self, session: Session):
        region_data = {"city": "Test City", "state": "Test State"}
        region = upsert_region(session, region_data)
        assert region.city == "Test City"
        assert region.state == "Test State"
        assert (
            session.query(Region)
            .filter_by(city="Test City", state="Test State")
            .count()
            == 1
        )

    def test_upsert_existing(self, session: Session):
        EXISTING_REGION_DATA = {"city": "Existing City", "state": "Existing State"}
        existing_region = Region(**EXISTING_REGION_DATA)
        session.add(existing_region)
        session.commit()

        region = upsert_region(session, EXISTING_REGION_DATA)
        assert region.id == existing_region.id
