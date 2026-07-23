from modules.repositories.game_repository import GameRepository


repository = GameRepository()

games = repository.get_all_games()

print("Gefundene Spiele:", len(games))

for game in games[:5]:
    print(game)