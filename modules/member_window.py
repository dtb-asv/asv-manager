import customtkinter as ctk
from tkinter import messagebox

from modules.widgets.calendar_entry import CalendarEntry
from modules.member_service import MemberService
from modules.widgets.change_reason_dialog import ChangeReasonDialog
from modules.lookup_service import LookupService
from modules.member_role_service import MemberRoleService


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
        self.geometry("650x600")
        self.grab_set()
        self.excel_datei = parent.excel_datei
        self.service = MemberService()
        self.member_role_service = MemberRoleService()
        self.lookup_service = LookupService()
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

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tab_allgemein = self.tabs.add("Allgemein")
        self.tab_rollen = self.tabs.add("Rollen")    

        self.vorname = ctk.CTkEntry(
            self.tab_allgemein,
            placeholder_text="Vorname *"
        )
        self.vorname.pack(fill="x", padx=30, pady=8)

        self.nachname = ctk.CTkEntry(
            self.tab_allgemein,
            placeholder_text="Nachname *"
        )
        self.nachname.pack(fill="x", padx=30, pady=8)

        self.geburtsdatum = CalendarEntry(
            self.tab_allgemein,
            label_text="Geburtsdatum *"
        )
        self.geburtsdatum.pack(fill="x", padx=30, pady=8)

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
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

        self.create_role_checkboxes()    
        self.load_existing_roles()

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

            dialog = ChangeReasonDialog(
                self,
                title="Mitglied ändern"
            )

            self.wait_window(dialog)

            if dialog.result is None:
                return

            daten["_GRUND"] = dialog.result["grund"]
            daten["_BEMERKUNG"] = dialog.result["bemerkung"]

            self.service.update_member(
                self.excel_datei,
                self.member_data["MEMBER_ID"],
                daten
            )

            self.member_role_service.save_roles(
                self.excel_datei,
                self.member_data["MEMBER_ID"],
                self.get_selected_role_codes()
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

    def create_role_checkboxes(self):

        rollen = self.lookup_service.get_lookup_list(
            self.excel_datei,
            "ROLE"
        )

        self.role_vars = {}

        for rolle in rollen:

            var = ctk.StringVar(value="0")

            cb = ctk.CTkCheckBox(
                self.tab_rollen,
                text=rolle,
                variable=var,
                onvalue="1",
                offvalue="0"
            )

            cb.pack(
                anchor="w",
                padx=20,
                pady=5
            )

            self.role_vars[rolle] = var    

    def get_selected_role_codes(self):

        role_codes = []

        for rolle, var in self.role_vars.items():

            if var.get() == "1":

                code = rolle.upper()
                code = code.replace("-", "_")
                code = code.replace(" ", "_")

                role_codes.append(code)

        return role_codes    

    def load_existing_roles(self):

        if not self.member_data:
            return

        df = self.member_role_service.load_roles(
            self.excel_datei,
            self.member_data["MEMBER_ID"]
        )

        if df.empty:
            return

        active_codes = set(
            df["ROLE_CODE"].astype(str).str.upper()
        )

        for rolle, var in self.role_vars.items():

            code = rolle.upper()
            code = code.replace("-", "_")
            code = code.replace(" ", "_")

            if code in active_codes:
                var.set("1")      


   