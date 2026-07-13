from modules.base.data_validator import DataValidator
from modules.constants import (
    SHEET_DEPARTMENTS,
    SHEET_MEMBERS,
    SHEET_TEAMS
)

excel_datei = "Excel/Terminefussball_2026_Herbst.xlsx"

validator = DataValidator()

validator.print_duplicate_report(
    excel_datei,
    SHEET_DEPARTMENTS,
    "DEPARTMENT_ID"
)

validator.print_duplicate_report(
    excel_datei,
    SHEET_MEMBERS,
    "MEMBER_ID"
)

validator.print_duplicate_report(
    excel_datei,
    SHEET_TEAMS,
    "TEAM_ID"
)