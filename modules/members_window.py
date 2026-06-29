import customtkinter as ctk

from modules.member_service import MemberService
from modules.member_window import MemberWindow
from tkinter import messagebox


class MembersWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei):
        super().__init__(parent)

        self.excel_datei = excel_datei
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

        df = self.service.load_members(self.excel_datei)
        df = df.dropna(how="all")

        if "STATUS" in df.columns:
            df = df[
                df["STATUS"].astype(str).str.lower() != "archiviert"
            ]

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
            f"{self.selected_member['NACHNAME']} archiviert werden?"
        )

        if not antwort:
            return

        self.service.archive_member(
            self.excel_datei,
            self.selected_member["MEMBER_ID"]
        )

        self.load_members()              