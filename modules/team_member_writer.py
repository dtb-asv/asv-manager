import pandas as pd

from modules.constants import SHEET_TEAM_MEMBERS


class TeamMemberWriter:

    def save(self, excel_datei, df):

        with pd.ExcelWriter(
            excel_datei,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace"
        ) as writer:

            df.to_excel(
                writer,
                sheet_name=SHEET_TEAM_MEMBERS,
                index=False
            )