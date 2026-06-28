import customtkinter as ctk

from modules.member_service import MemberService
from modules.member_window import MemberWindow


class MembersWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.service = MemberService()

        self.title("Mitglieder")
        self.geometry("1000x650")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="👥 Mitglieder",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=15)

        ctk.CTkButton(
            self,
            text="➕ Neues Mitglied",
            command=self.neues_mitglied
        ).pack(pady=5)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkButton(
            self,
            text="❌ Schließen",
            command=self.destroy
        ).pack(pady=15)

        self.load_members()

    def load_members(self):

        df = self.service.load_members(self.excel_datei)
        df = df.dropna(how="all")

        columns = [
            "MEMBER_ID",
            "VORNAME",
            "NACHNAME",
            "GEBURTSDATUM",
            "STATUS"
        ]

        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x", pady=(0, 5))

        for col in columns:
            ctk.CTkLabel(
                header,
                text=col,
                width=150,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=3)

        for _, row in df.iterrows():

            row_frame = ctk.CTkFrame(self.scroll)
            row_frame.pack(fill="x", pady=2)

            for col in columns:
                ctk.CTkLabel(
                    row_frame,
                    text=str(row.get(col, "")),
                    width=150,
                    font=("Segoe UI", 12)
                ).pack(side="left", padx=3)

    def neues_mitglied(self):

        MemberWindow(self)                