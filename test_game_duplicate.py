from modules.repositories.game_repository import GameRepository


repository = GameRepository()

existing_key = "TEST-U10-2026-09-05-1000"
unknown_key = "DIESER-SCHLUESSEL-EXISTIERT-NICHT"

print(
    "Vorhandener Schlüssel:",
    repository.exists_by_source_key(existing_key)
)

print(
    "Unbekannter Schlüssel:",
    repository.exists_by_source_key(unknown_key)
)