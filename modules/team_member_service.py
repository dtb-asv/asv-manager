import pandas as pd

from modules.constants import SHEET_TEAM_MEMBERS
from modules.base.service_base import ServiceBase
from modules.constants import SHEET_TEAM_MEMBERS
from modules.constants import SHEET_MEMBERS
from modules.constants import SHEET_MEMBER_ROLES
from modules.team_member_writer import TeamMemberWriter
from modules.repositories.team_member_repository import TeamMemberRepository


class TeamMemberService(ServiceBase):

    def __init__(self):

        super().__init__()

        self.repository = TeamMemberRepository()
        self.writer = TeamMemberWriter()

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
            how="inner",
            suffixes=("", "_MEMBER")
        )

        return result.sort_values(
            ["NACHNAME", "VORNAME"]
        )

    
    def assign_player(
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

        next_number = 1

        if not df.empty and "TEAM_MEMBER_ID" in df.columns:

            numbers = []

            for value in df["TEAM_MEMBER_ID"].dropna():

                text = str(value)

                if text.startswith("TM"):

                    try:
                        numbers.append(
                            int(text.replace("TM", ""))
                        )
                    except ValueError:
                        pass

            next_number = max(numbers, default=0) + 1

        new_row = {
            "TEAM_MEMBER_ID": f"TM{next_number:06d}",
            "TEAM_ID": team_id,
            "MEMBER_ID": member_id,
            "ROLLE": "SPIELER",
            "VON": "",
            "BIS": "",
            "AKTIV": "Ja",
            "BEMERKUNG": ""
        }

        df = pd.concat(
            [
                df,
                pd.DataFrame([new_row])
            ],
            ignore_index=True
        )

        self.writer.save(
            excel_datei,
            df
        )

        return True   

    def remove_player(
        self,
        excel_datei,
        team_member_id
    ):

        df = self.load_sheet(
            excel_datei,
            SHEET_TEAM_MEMBERS
        )

        index = df[
            df["TEAM_MEMBER_ID"].astype(str)
            == str(team_member_id)
        ].index

        if len(index) == 0:
            return False

        df.loc[index[0], "AKTIV"] = "Nein"

        self.writer.save(
            excel_datei,
            df
        )

        return True

    def get_all_staff(self, excel_datei):

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

        allowed_roles = [
            "TRAINER",
            "CO_TRAINER",
            "TORMANNTRAINER",
            "BETREUER"
        ]

        roles = roles[
            roles["ROLE_CODE"]
            .astype(str)
            .str.upper()
            .isin(allowed_roles)
        ]

        result = members.merge(
            roles[["MEMBER_ID", "ROLE_CODE"]],
            on="MEMBER_ID",
            how="inner"
        )

        return result.sort_values(
            ["NACHNAME", "VORNAME", "ROLE_CODE"]
        )    

    def assign_staff(
        self,
        excel_datei,
        team_id,
        member_id,
        role_code
    ):

        df = self.load_sheet(
            excel_datei,
            SHEET_TEAM_MEMBERS
        )

        role_code = str(role_code).strip().upper()

        if not df.empty:

            existing = df[
                (df["TEAM_ID"].astype(str) == str(team_id))
                &
                (df["MEMBER_ID"].astype(str) == str(member_id))
                &
                (df["ROLLE"].astype(str).str.upper() == role_code)
                &
                (df["AKTIV"].astype(str).str.upper() == "JA")
            ]

            if not existing.empty:
                return False

        numbers = []

        if not df.empty and "TEAM_MEMBER_ID" in df.columns:

            for value in df["TEAM_MEMBER_ID"].dropna():

                text = str(value)

                if text.startswith("TM"):

                    try:
                        numbers.append(
                            int(text.replace("TM", ""))
                        )
                    except ValueError:
                        pass

        next_number = max(numbers, default=0) + 1

        new_row = {
            "TEAM_MEMBER_ID": f"TM{next_number:06d}",
            "TEAM_ID": team_id,
            "MEMBER_ID": member_id,
            "ROLLE": role_code,
            "VON": "",
            "BIS": "",
            "AKTIV": "Ja",
            "BEMERKUNG": ""
        }

        df = pd.concat(
            [
                df,
                pd.DataFrame([new_row])
            ],
            ignore_index=True
        )

        self.writer.save(
            excel_datei,
            df
        )

        return True    

    def get_team_staff(
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

        allowed_roles = [
            "TRAINER",
            "CO_TRAINER",
            "TORMANNTRAINER",
            "BETREUER"
        ]

        assignments = assignments[
            assignments["ROLLE"]
            .astype(str)
            .str.upper()
            .isin(allowed_roles)
        ]

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
            how="inner",
            suffixes=("", "_MEMBER")
        )

        return result.sort_values(
            ["ROLLE", "NACHNAME", "VORNAME"]
        )   

    def get_all_players_db(self):
        return self.repository.get_all_players()


    def get_team_players_db(self, team_id):
        return self.repository.get_team_players(team_id)


    def assign_player_db(self, team_id, person_id):
        return self.repository.assign_player(
            team_id,
            person_id
        )


    def remove_player_db(self, team_member_id):
        return self.repository.remove_player(
            team_member_id
        )     

    def get_all_staff_db(self):
        return self.repository.get_all_staff()


    def get_team_staff_db(self, team_id):
        return self.repository.get_team_staff(team_id)


    def assign_staff_db(self, team_id, person_id):
        return self.repository.assign_staff(
            team_id,
            person_id
        )


    def remove_staff_db(self, team_member_id):
        return self.repository.remove_staff(
            team_member_id
        )    