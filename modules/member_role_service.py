import pandas as pd

from modules.constants import SHEET_MEMBER_ROLES
from modules.member_role_writer import MemberRoleWriter


class MemberRoleService:

    def __init__(self):
        self.writer = MemberRoleWriter()
    
    def load_roles(self, excel_datei, member_id):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_MEMBER_ROLES
        )

        if df.empty:
            return df

        df = df[
            df["MEMBER_ID"] == member_id
        ]

        if "AKTIV" in df.columns:
            df = df[
                df["AKTIV"].astype(str).str.upper() == "JA"
            ]

        return df

    def save_roles(
        self,
        excel_datei,
        member_id,
        role_codes
    ):

        self.writer.deactivate_roles(
            excel_datei,
            member_id
        )

        for role_code in role_codes:

            self.writer.add_role(
                excel_datei,
                member_id,
                role_code
            )    