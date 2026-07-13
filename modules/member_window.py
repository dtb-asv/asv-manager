import customtkinter as ctk
from tkinter import messagebox

from modules.widgets.calendar_entry import CalendarEntry
from modules.member_service import MemberService
from modules.widgets.change_reason_dialog import ChangeReasonDialog
from modules.lookup_service import LookupService
from modules.member_role_service import MemberRoleService
from modules.base.edit_window_base import EditWindowBase
from datetime import datetime


class MemberWindow(EditWindowBase):

    def __init__(
        self,
        parent,
        on_saved=None,
        member_data=None
    ):
        
        super().__init__(
            parent,
            title="👥 Mitglied",
            width=900,
            height=750
        )

        if member_data:
            self.set_save_text("Änderungen speichern")
        else:
            self.set_save_text("Speichern")

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
            self.show_id(
                self.member_data["MEMBER_ID"]
            )

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tab_allgemein = self.add_tab("Allgemein")

        content = ctk.CTkFrame(
            self.tab_allgemein,
            fg_color="transparent"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        left = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        right = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,10)
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10,0)
        )

        self.tab_rollen = self.add_tab("Rollen") 

        self.vorname = ctk.CTkEntry(
            left,
            placeholder_text="Vorname *"
        )
        self.vorname.pack(fill="x", padx=30, pady=8)

        self.nachname = ctk.CTkEntry(
            left,
            placeholder_text="Nachname *"
        )
        self.nachname.pack(fill="x", padx=30, pady=8)

        self.geburtsdatum = CalendarEntry(
            left,
            label_text="Geburtsdatum *"
        )
        self.geburtsdatum.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(
            left,
            text="Geschlecht"
        ).pack(anchor="w", padx=30)

        self.geschlecht = ctk.CTkComboBox(
            left,
            values=[
                "Männlich",
                "Weiblich",
                "Divers"
            ]
        )
        self.geschlecht.pack(fill="x", padx=30, pady=8)
        self.geschlecht.set("Männlich")

        ctk.CTkLabel(
            right,
            text="Mobilnummer"
        ).pack(anchor="w", padx=30)

        self.mobil = ctk.CTkEntry(
            right,
            placeholder_text="z.B. 0664 1234567"
        )

        self.mobil.pack(
            fill="x",
            padx=30,
            pady=8
        )

        ctk.CTkLabel(
            right,
            text="E-Mail"
        ).pack(anchor="w", padx=30)

        self.email = ctk.CTkEntry(
            right,
            placeholder_text="name@beispiel.at"
        )

        self.email.pack(
            fill="x",
            padx=30,
            pady=8
        )

        self.eintritt = CalendarEntry(
            right,
            label_text="Eintritt"
        )
        self.eintritt.pack(fill="x", padx=30, pady=8)

        self.austritt = CalendarEntry(
            right,
            label_text="Austritt"
        )
        self.austritt.pack(fill="x", padx=30, pady=8)

        if not self.member_data:

            self.eintritt.set(
                datetime.now().strftime("%d.%m.%Y")
            )
            self.austritt.set("31.12.9999")

            self.eintritt.set_enabled(False)
            self.austritt.set_enabled(False)

        else:

            self.eintritt.set_enabled(True)
            self.austritt.set_enabled(True)

        ctk.CTkLabel(
            right,
            text="Spielerpassnummer"
        ).pack(anchor="w", padx=30)

        self.spielerpassnummer = ctk.CTkEntry(
            right,
            placeholder_text="Spielerpassnummer"
        )

        self.spielerpassnummer.pack(
            fill="x",
            padx=30,
            pady=8
        )

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
            "GEBURTSDATUM": self.geburtsdatum.get(),
            "GESCHLECHT": self.geschlecht.get(),
            "MOBIL": self.mobil.get().strip(),
            "EINTRITT": self.eintritt.get(),
            "AUSTRITT": self.austritt.get(),
            "SPIELERPASSNUMMER": self.spielerpassnummer.get().strip(),
            "EMAIL": self.email.get().strip()
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
            member_id = self.service.add_member(
                self.excel_datei,
                daten
            )

            self.member_role_service.save_roles(
                self.excel_datei,
                member_id,
                self.get_selected_role_codes()
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

        self.geschlecht.set(
            self.member_data.get("GESCHLECHT", "Männlich")
        )

        self.mobil.insert(
            0,
            self.member_data.get("MOBIL", "")
        )

        eintritt = self.member_data.get("EINTRITT", "")

        if str(eintritt).lower() != "nan":
            self.eintritt.set(eintritt)

        austritt = self.member_data.get("AUSTRITT", "")

        if str(austritt).lower() != "nan":
            self.austritt.set(austritt)

        self.spielerpassnummer.insert(
            0,
            self.member_data.get("SPIELERPASSNUMMER", "")
        )

        self.email.insert(
            0,
            self.member_data.get("EMAIL", "")
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

        if not hasattr(self, "role_vars"):
            return []

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

    def on_save(self):

        self.speichern()               


   