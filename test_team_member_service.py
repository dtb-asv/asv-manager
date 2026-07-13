from modules.team_member_service import TeamMemberService

excel_datei = "Excel/Terminefussball_2026_Herbst.xlsx"

service = TeamMemberService()

df = service.get_all_players(excel_datei)

print(df.columns.tolist())

print(df[[
    "VORNAME",
    "NACHNAME"
]])