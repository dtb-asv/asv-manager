from datetime import date, time

from modules.repositories.game_repository import GameRepository


repository = GameRepository()

season_id = repository.get_active_season()
team_id = repository.get_team_id(season_id, "U10")
place_id = repository.get_place_id("Hauptplatz")

game_id = repository.insert_game(
    season_id=season_id,
    team_id=team_id,
    place_id=place_id,
    round_number=1,
    game_date=date(2026, 9, 5),
    start_time=time(10, 0),
    end_time=time(11, 30),
    opponent="TESTGEGNER",
    home_away="Heim",
    game_type="Testspiel",
    status="Aktiv",
    notes="Testeintrag für GameRepository",
    source_file="test_game_insert.py",
    source_sheet="TEST",
    source_row=1,
    source_key="TEST-U10-2026-09-05-1000",
)

print("Neues Spiel angelegt. GAME_ID:", game_id)