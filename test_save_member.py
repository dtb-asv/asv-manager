from pathlib import Path

from modules.importers.member_import_service import MemberImportService
from modules.repositories.member_repository import MemberRepository

service = MemberImportService()
repo = MemberRepository()

datei = Path("data") / "ASV_Mitglieder 2026-2027.xlsx"

df = service.load_preview(datei)

mitglied = df.iloc[0]

print("Speichere:")
print(mitglied)

repo.save(mitglied)

print()
print("Anzahl Personen:", repo.count())