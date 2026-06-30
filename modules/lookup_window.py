import customtkinter as ctk

from modules.lookup_service import LookupService


class LookupWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        excel_datei,
        lookup_type,
        title
    ):

        super().__init__(parent)

        self.excel_datei = excel_datei
        self.lookup_type = lookup_type

        self.service = LookupService()

        self.title(title)
        self.geometry("850x600")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self)

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_data()

    def load_data(self):

        df = self.service.load_by_type(
            self.excel_datei,
            self.lookup_type
        )

        columns = [
            "CODE",
            "NAME",
            "BESCHREIBUNG",
            "AKTIV"
        ]

        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x")

        for col in columns:

            ctk.CTkLabel(
                header,
                text=col,
                width=180,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left")

        for _, row in df.iterrows():

            frame = ctk.CTkFrame(self.scroll)

            frame.pack(
                fill="x",
                pady=2
            )

            for col in columns:

                ctk.CTkLabel(
                    frame,
                    text=str(row.get(col, "")),
                    width=180
                ).pack(side="left")    