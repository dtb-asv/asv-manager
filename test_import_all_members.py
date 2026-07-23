from pathlib import Path

from modules.importers.member_import_service import MemberImportService
from modules.repositories.member_repository import MemberRepository


service = MemberImportService()
repo = MemberRepository()

datei = Path("data") / "ASV_Mitglieder 2026-2027.xlsx"

df = service.load_preview(datei)

members = df.to_dict(orient="records")

result = repo.save_many(members)

print()
print("==============================")
print("IMPORT ABGESCHLOSSEN")
print("==============================")
print(f"Neu angelegt          : {result['inserted']}")
print(f"Aktualisiert          : {result['updated']}")
print(f"ID neu zugeordnet     : {result['reassigned']}")
print(f"Personen in Datenbank : {repo.count()}")