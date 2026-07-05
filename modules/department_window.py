import customtkinter as ctk

from modules.widgets.list_window_base import ListWindowBase
from modules.department_service import DepartmentService


class DepartmentWindow(ListWindowBase):

    def __init__(self, parent, excel_datei):

        self.service = DepartmentService()

        super().__init__(
            parent,
            title="Bereiche",
            icon="🏢",
            search_placeholder="Bereich suchen...",
            search_callback=self.load_data
        )

        self.excel_datei = excel_datei

        self.load_data()

    def load_data(self, suchtext=""):

        df = self.service.load_departments(
            self.excel_datei
        )

        self.set_dataframe(df)    