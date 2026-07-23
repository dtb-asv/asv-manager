import customtkinter as ctk
import pandas as pd

from modules.member_service import MemberService
from modules.member_window import MemberWindow
from tkinter import messagebox
from modules.widgets.search_bar import SearchBar
from modules.widgets.list_toolbar import ListToolbar


class MembersWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.service = MemberService()
        self.selected_member = None
        self.selected_frame = None

        self.title("Mitglieder")
        self.geometry("1000x650")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="👥 Mitglieder",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=15)

        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        toolbar.pack(pady=5)

        self.search = SearchBar(
            self,
            callback=self.filter_members,
            placeholder="Mitglieder suchen..."
        )

        self.search.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        ctk.CTkButton(
            toolbar,
            text="➕ Neu",
            command=self.neues_mitglied,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="✏ Bearbeiten",
            command=self.bearbeiten_mitglied,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="📦 Archivieren",
            command=self.archivieren_placeholder,
            width=140
        ).pack(side="left", padx=5)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkButton(
            self,
            text="❌ Schließen",
            command=self.destroy
        ).pack(pady=15)

        self.load_members()

    def load_members(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.selected_member = None
        self.selected_frame = None

        members = self.service.get_all()

        rows = []

        for member in members:
            rows.append({
                "MEMBER_ID": member["external_member_id"],
                "VORNAME": member["first_name"],
                "NACHNAME": member["last_name"],
                "GEBURTSDATUM": member["birth_date"],
                "STATUS": "Aktiv",
                "PERSON_ID": member["person_id"],
            })

        self.df = pd.DataFrame(rows)

        self.draw_members(self.df)

    def draw_members(self, df):

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

            row_data = row.to_dict()

            row_frame = ctk.CTkFrame(
                self.scroll,
                fg_color="transparent"
            )
            row_frame.pack(fill="x", pady=2)

            row_frame.bind(
                "<Button-1>",
                lambda event, r=row_data, f=row_frame: self.select_member(r, f)
            )

            row_frame.bind(
                "<Double-Button-1>",
                lambda event: self.bearbeiten_mitglied()
            )

            for col in columns:

                label = ctk.CTkLabel(
                    row_frame,
                    text=str(row.get(col, "")),
                    width=150,
                    font=("Segoe UI", 12)
                )

                label.pack(side="left", padx=3)

                label.bind(
                    "<Button-1>",
                    lambda event, r=row_data, f=row_frame: self.select_member(r, f)
                )   

                label.bind(
                    "<Double-Button-1>",
                    lambda event: self.bearbeiten_mitglied()
                )         
                
    def neues_mitglied(self):

        MemberWindow(
            self,
            on_saved=self.load_members
        ) 

    def select_member(self, row, frame):

        if self.selected_frame:
            self.selected_frame.configure(
                fg_color="transparent"
            )

        frame.configure(
            fg_color=("lightblue", "#1F538D")
        )

        self.selected_frame = frame
        self.selected_member = row

        print(self.selected_member)     

    def bearbeiten_mitglied(self):

        if self.selected_member is None:
            print("Bitte zuerst ein Mitglied auswählen.")
            return

        MemberWindow(
            self,
            on_saved=self.load_members,
            member_data=self.selected_member
        )


    def archivieren_placeholder(self):

        if self.selected_member is None:
            messagebox.showwarning(
                "Kein Mitglied",
                "Bitte zuerst ein Mitglied auswählen."
            )
            return

        antwort = messagebox.askyesno(
            "Mitglied archivieren",
            f"Soll {self.selected_member['VORNAME']} "
            f"{self.selected_member['NACHNAME']} archiviert werden?",
            parent=self
        )

        if not antwort:
            return

        self.service.archive_member(
            self.selected_member["PERSON_ID"]
        )

        self.load_members()

    def filter_members(self, text):

        text = text.strip().lower()

        # Aktuelle Anzeige leeren
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.selected_member = None
        self.selected_frame = None

        df = self.df.copy()

        if text == "":
            self.draw_members(df)
            return

        mask = (
            df["VORNAME"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(text, regex=False)
            |
            df["NACHNAME"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(text, regex=False)
            |
            df["MEMBER_ID"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(text, regex=False)
        )

        self.draw_members(df[mask])