from modules.repositories.team_repository import TeamRepository

repo = TeamRepository()

print("===========================")
print("MANNSCHAFTEN")
print("===========================")

print("Anzahl:", repo.count())

print()

for team in repo.get_all():
    print(team)