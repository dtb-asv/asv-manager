from modules.repositories.place_repository import PlaceRepository


class PlaceService:

    def __init__(self):

        self.repository = PlaceRepository()

    def get_all(self):

        return self.repository.get_all()

    def get_active(self):

        return self.repository.get_active()

    def get_by_id(self, place_id):

        return self.repository.get_by_id(place_id)

    def save_place(self, daten):

        place = {

            "place_id": daten.get(
                "place_id",
                daten.get("PLACE_ID")
            ),

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

            "training_zones": daten.get(
                "training_zones",
                daten.get("TRAINING_ZONES", "")
            ),

            "active": daten.get(
                "active",
                daten.get("AKTIV", True)
            )
        }

        if isinstance(place["active"], str):

            place["active"] = (
                place["active"].strip().lower()
                in ("ja", "true", "1", "aktiv")
            )

        return self.repository.save(place)
    def archive_place(self, place_id):

        self.repository.archive(place_id)