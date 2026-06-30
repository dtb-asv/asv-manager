from modules.excel_reader import ExcelReader
from modules.role_writer import RoleWriter
from modules.constants import SHEET_CFG_ROLES


class RoleService:

    def __init__(self):

        self.reader = ExcelReader()
        self.writer = RoleWriter()

    def load_roles(self, excel_datei):

        self.reader.load(
            excel_datei,
            sheet=SHEET_CFG_ROLES
        )

        return self.reader.df.copy()

    def add_role(self, excel_datei, daten):

        self.writer.add_role(
            excel_datei,
            daten
        )


    def update_role(
        self,
        excel_datei,
        role_id,
        daten
    ):

        self.writer.update_role(
            excel_datei,
            role_id,
            daten
        )


    def archive_role(
        self,
        excel_datei,
        role_id
    ):

        self.writer.archive_role(
            excel_datei,
            role_id
        )    