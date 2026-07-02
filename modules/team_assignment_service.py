import pandas as pd

from modules.constants import SHEET_TEAM_ASSIGNMENTS
from modules.team_assignment_writer import TeamAssignmentWriter


class TeamAssignmentService:

    def __init__(self):
        self.writer = TeamAssignmentWriter()

    def load_assignments(self, excel_datei, team_id=None, member_id=None):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_TEAM_ASSIGNMENTS
        )

        if df.empty:
            return df

        if team_id is not None:
            df = df[
                df["TEAM_ID"] == team_id
            ]

        if member_id is not None:
            df = df[
                df["MEMBER_ID"] == member_id
            ]

        if "AKTIV" in df.columns:
            df = df[
                df["AKTIV"].astype(str).str.upper() == "JA"
            ]

        return df

    def save_assignments(
        self,
        excel_datei,
        team_id,
        assignments
    ):

        self.writer.deactivate_assignments(
            excel_datei,
            team_id
        )

        for member_id, role_code in assignments:

            self.writer.add_assignment(
                excel_datei,
                team_id,
                member_id,
                role_code
            )    