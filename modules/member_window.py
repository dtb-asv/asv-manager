import customtkinter as ctk
from tkinter import messagebox

from modules.widgets.calendar_entry import CalendarEntry
from modules.member_service import MemberService


class MemberWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        
        super().__init__(parent)

        self.title("Neues Mitglied")
        self.geometry("450x420")
        self.grab_set()
        self.excel_datei = parent.excel_datei
        self.service = MemberService()

        ctk.CTkLabel(
            self,
            text="👥 Neues Mitglied",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        self.vorname = ctk.CTkEntry(
            self,
            placeholder_text="Vorname *"
        )
        self.vorname.pack(fill="x", padx=30, pady=8)

        self.nachname = ctk.CTkEntry(
            self,
            placeholder_text="Nachname *"
        )
        self.nachname.pack(fill="x", padx=30, pady=8)

        self.geburtsdatum = CalendarEntry(
            self,
            label_text="Geburtsdatum *"
        )
        self.geburtsdatum.pack(fill="x", padx=30, pady=8)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=25)

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Speichern",
            command=self.speichern
        ).pack(side="left", padx=10)

    def speichern(self):

        if not self.vorname.get().strip():
            messagebox.showwarning(
                "Pflichtfeld",
                "Bitte Vorname eingeben."
            )
            return

        if not self.nachname.get().strip():
            messagebox.showwarning(
                "Pflichtfeld",
                "Bitte Nachname eingeben."
            )
            return

        daten = {
            "VORNAME": self.vorname.get().strip(),
            "NACHNAME": self.nachname.get().strip(),
            "GEBURTSDATUM": self.geburtsdatum.get()
        }

        self.service.add_member(
            self.excel_datei,
            daten
        )

        self.destroy()


   