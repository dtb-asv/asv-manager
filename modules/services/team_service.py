from modules.repositories.team_repository import TeamRepository


class TeamService:

    def __init__(self):
        self.repo = TeamRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_active(self):
        return self.repo.get_active()

    def count(self):
        return self.repo.count()

    def delete(self, team_id):
        self.repo.delete(team_id)    