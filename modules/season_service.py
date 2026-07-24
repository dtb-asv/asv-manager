from modules.repositories.season_repository import SeasonRepository


class SeasonService:

    def __init__(self):
        self.repository = SeasonRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_active(self):
        return self.repository.get_active()

    def create_season(self, name, active=True):
        return self.repository.save(
            name=name,
            active=active
        )

    def get_season(self, season_id):
        return self.repository.get_by_id(season_id)



    def update_season(self, season_id, name, active=True):
        self.repository.update(
            season_id=season_id,
            name=name,
            active=active
        )
