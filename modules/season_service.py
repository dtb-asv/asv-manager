from modules.repositories.season_repository import SeasonRepository


class SeasonService:

    def __init__(self):
        self.repository = SeasonRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_active(self):
        return self.repository.get_active()