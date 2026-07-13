import pandas as pd

from modules.constants import SHEET_TEAM_MEMBERS
from modules.base.service_base import ServiceBase
from modules.constants import SHEET_TEAM_MEMBERS
from modules.constants import SHEET_MEMBERS
from modules.constants import SHEET_MEMBER_ROLES


class TeamMemberService(ServiceBase):

    def load_assignments(self, excel_datei, team_id):

        from modules.constants import (
            SHEET_TEAM_MEMBERS,
            SHEET_MEMBERS
        )

        df = self.load_sheet(
            excel_datei,
            SHEET_TEAM_MEMBERS
        )

        if df.empty:
            return df

        df = df[
            df["TEAM_ID"].astype(str) == str(team_id)
        ]

        df = self.active_only(df)

        return df

    def get_all_players(self, excel_datei):

        members = self.load_sheet(
            excel_datei,
            SHEET_MEMBERS
        )

        roles = self.load_sheet(
            excel_datei,
            SHEET_MEMBER_ROLES
        )

        members = self.active_only(
            members,
            status_column="STATUS"
        )

        roles = self.active_only(roles)

        roles = roles[
            roles["ROLE_CODE"].astype(str).str.upper() == "SPIELER"
        ]

        result = members.merge(
            roles[["MEMBER_ID", "ROLE_CODE"]],
            on="MEMBER_ID",
            how="inner"
        )

        return result.sort_values(
            ["NACHNAME", "VORNAME"]
        )

    def get_team_players(
        self,
        excel_datei,
        team_id
    ):

        assignments = self.load_assignments(
            excel_datei,
            team_id
        )

        if assignments.empty:
            return assignments

        members = self.load_sheet(
            excel_datei,
            SHEET_MEMBERS
        )

        members = members[
            members["STATUS"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "aktiv"
        ]

        result = assignments.merge(
            members,
            on="MEMBER_ID",
            how="inner"
        )

        return result.sort_values(
            ["NACHNAME", "VORNAME"]
        )

    def add_player_to_team(
        self,
        excel_datei,
        team_id,
        member_id
    ):

        df = self.load_sheet(
            excel_datei,
            SHEET_TEAM_MEMBERS
        )

        if not df.empty:

            existing = df[
                (df["TEAM_ID"].astype(str) == str(team_id))
                &
                (df["MEMBER_ID"].astype(str) == str(member_id))
                &
                (df["ROLLE"].astype(str).str.upper() == "SPIELER")
                &
                (df["AKTIV"].astype(str).str.upper() == "JA")
            ]

            if not existing.empty:
                return False

        return True        