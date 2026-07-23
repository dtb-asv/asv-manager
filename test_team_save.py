from modules.repositories.team_repository import TeamRepository

repo = TeamRepository()

team_id = repo.save(
    name="U10",
    season_id=1,
    active=True
)

print("Neue Team-ID:", team_id)
print("Anzahl Teams:", repo.count())

print()

for team in repo.get_all():
    print(team)