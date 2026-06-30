import customtkinter as ctk

from modules.lookup_service import LookupService


class LookupComboBox(ctk.CTkComboBox):

    def __init__(
        self,
        parent,
        excel_datei,
        lookup_type,
        **kwargs
    ):

        self.service = LookupService()

        values = self.service.get_lookup_list(
            excel_datei,
            lookup_type
        )

        super().__init__(
            parent,
            values=values,
            **kwargs
        )

        if values:
            self.set(values[0])