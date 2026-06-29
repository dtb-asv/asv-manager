import customtkinter as ctk
from tkinter import messagebox

from modules.widgets.calendar_entry import CalendarEntry
from modules.member_service import MemberService


class MemberWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        on_saved=None,
        member_data=None
    ):
        
        super().__init__(parent)

        if member_data:
            self.title("Mitglied bearbeiten")
        else:
            self.title("Neues Mitglied")
        self.geometry("450x420")
        self.grab_set()
        self.excel_datei = parent.excel_datei
        self.service = MemberService()
        self.on_saved = on_saved
        self.member_data = member_data

        titel = "👥 Neues Mitglied"

        if member_data:
            titel = "✏ Mitglied bearbeiten"

        ctk.CTkLabel(
            self,
            text=titel,
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        if self.member_data:

            ctk.CTkLabel(
                self,
                text=f"🆔 {self.member_data['MEMBER_ID']}",
                font=("Segoe UI", 15, "bold"),
                text_color=("gray30", "gray80")
            ).pack(pady=(0, 15))

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

        button_text = "Speichern"

        if member_data:
            button_text = "Änderungen speichern"

        ctk.CTkButton(
            button_frame,
            text=button_text,
            command=self.speichern
        ).pack(side="left", padx=10)

        if self.member_data:
            self.fill_data()

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

        if self.member_data:
            self.service.update_member(
                self.excel_datei,
                self.member_data["MEMBER_ID"],
                daten
            )
        else:
            self.service.add_member(
                self.excel_datei,
                daten
            )

        if self.on_saved:
            self.on_saved()

        self.destroy()

    def fill_data(self):

        self.vorname.insert(
            0,
            self.member_data["VORNAME"]
        )

        self.nachname.insert(
            0,
            self.member_data["NACHNAME"]
        )

        self.geburtsdatum.set(
            self.member_data["GEBURTSDATUM"]
        )    


   