from pathlib import Path

from modules.importers.member_import_service import (
    MemberImportService,
)


service = MemberImportService()

datei = (
    Path("data")
    / "ASV_Mitglieder 2026-2027.xlsx"
)

df = service.load_preview(datei)
stats = service.statistics(df)

print("====================================")
print("MITGLIEDER IMPORTVORSCHAU")
print("====================================")
print(f"Gültige Mitglieder     : {stats['rows']}")
print(f"Mit Geburtsdatum       : {stats['valid_birth_dates']}")
print(f"Ohne Geburtsdatum      : {stats['missing_birth_dates']}")
print(f"Mögliche Dubletten     : {stats['duplicates']}")
print()

print("Erste 10 Datensätze:")
print(
    df.head(10).to_string(
        index=False
    )
)
print()
print("====================================")
print("MITGLIEDER OHNE GEBURTSDATUM")
print("====================================")

ohne_geburtstag = df[df["Geburtstag"].isna()]

if ohne_geburtstag.empty:
    print("Keine")
else:
    print(ohne_geburtstag.to_string(index=False))


print()
print("====================================")
print("MÖGLICHE DUBAllETTEN")
print("====================================")

dubletten = df[
    df.duplicated(
        subset=["Vorname", "Nachname", "Geburtstag"],
        keep=False
    )
].sort_values(
    ["Nachname", "Vorname", "Geburtstag"]
)

if dubletten.empty:
    print("Keine")
else:
    print(dubletten.to_string(index=False))