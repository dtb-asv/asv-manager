import customtkinter as ctk

from modules.role_service import RoleService


class RolesWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.service = RoleService()

        self.title("Rollen")
        self.geometry("800x600")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="⚙ Rollen",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_roles()

    def load_roles(self):

        df = self.service.load_roles(self.excel_datei)

        columns = [
            "ROLE_ID",
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
            frame.pack(fill="x", pady=2)

            for col in columns:

                ctk.CTkLabel(
                    frame,
                    text=str(row.get(col, "")),
                    width=180
                ).pack(side="left")