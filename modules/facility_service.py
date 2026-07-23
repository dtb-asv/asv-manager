from modules.repositories.facility_repository import FacilityRepository


class FacilityService:

    def __init__(self):

        self.repository = FacilityRepository()

    def get_all(self):

        return self.repository.get_all()

    def get_active(self):

        return self.repository.get_active()

    def get_by_id(self, facility_id):

        return self.repository.get_by_id(facility_id)

    def save_facility(self, daten):

        facility = {

            "facility_id": daten.get(
                "facility_id",
                daten.get("FACILITY_ID")
            ),

            "name": daten.get(
                "name",
                daten.get("NAME", "")
            ),

            "address": daten.get(
                "address",
                daten.get("ADDRESS", "")
            ),

            "active": daten.get(
                "active",
                daten.get("AKTIV", True)
            )
        }

        if isinstance(facility["active"], str):

            facility["active"] = (
                facility["active"].strip().lower()
                in ("ja", "true", "1", "aktiv")
            )

        return self.repository.save(facility)

    def archive_facility(self, facility_id):

        self.repository.archive(facility_id)