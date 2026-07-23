from modules.repositories.game_repository import GameRepository


repository = GameRepository()

season_id = repository.get_active_season()

print("Aktive Saison:", season_id)

if season_id is None:
    print("FEHLER: Keine aktive Saison gefunden.")
else:
    team_id = repository.get_team_id(
        season_id,
        "U10"
    )

    print("Team U10:", team_id)

place_id = repository.get_place_id(
    "Hauptplatz"
)

print("Platz Hauptplatz:", place_id)