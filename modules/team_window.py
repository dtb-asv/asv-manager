import customtkinter as ctk
from modules.team_service import TeamService
from tkinter import messagebox
from modules.widgets.change_reason_dialog import ChangeReasonDialog
from modules.member_service import MemberService
from modules.lookup_service import LookupService
from modules.team_assignment_service import TeamAssignmentService
from modules.widgets.assignment_widget import AssignmentWidget


class TeamWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        excel_datei,
        on_saved=None,
        team_data=None
    ):

        super().__init__(parent)

        self.excel_datei = excel_datei
        self.on_saved = on_saved
        self.service = TeamService()
        self.member_service = MemberService()
        self.lookup_service = LookupService()
        self.assignment_service = TeamAssignmentService()
        self.team_data = team_data

        if team_data:
            self.title("Mannschaft bearbeiten")
        else:
            self.title("Neue Mannschaft")
        self.geometry("700x600")

        self.grab_set()

        titel = "⚽ Neue Mannschaft"

        if team_data:
            titel = "✏ Mannschaft bearbeiten"

        ctk.CTkLabel(
            self,
            text=titel,
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        self.tabs = ctk.CTkTabview(self)

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tab_allgemein = self.tabs.add("Allgemein")
        self.tab_mitglieder = self.tabs.add("Mitglieder")
        self.tab_vereine = self.tabs.add("Vereine")
        self.tab_history = self.tabs.add("History")

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Mannschaft"
        ).pack(anchor="w", padx=20)

        self.name = ctk.CTkEntry(
            self.tab_allgemein,
            width=300
        )

        self.name.pack(
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Saison"
        ).pack(anchor="w", padx=20)

        self.saison = ctk.CTkComboBox(
            self.tab_allgemein,
            width=300,
            values=[
                "2025/2026",
                "2026/2027",
                "2027/2028"
            ]
        )
        self.saison.pack(
            padx=20,
            pady=(0, 10)
        )

        self.saison.set("2026/2027")

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Typ"
        ).pack(anchor="w", padx=20)

        self.typ = ctk.CTkComboBox(
            self.tab_allgemein,
            width=300,
            values=[
                "Normal",
                "Spielgemeinschaft",
                "Mädchen",
                "Fußballkindergarten"
            ]
        )

        self.typ.pack(
            padx=20,
            pady=(0, 20)
        )

        self.typ.set("Normal")

        if self.team_data:

            self.name.insert(
                0,
                self.team_data.get("MANNSCHAFT", "")
            )

            self.saison.set(
                self.team_data.get("SAISON", "2026/2027")
            )

            self.typ.set(
                self.team_data.get("TYP", "Normal")
            )
        
        self.create_member_tab()

        ctk.CTkButton(
            self,
            text="Speichern",
            command=self.speichern
        ).pack(pady=20)

    def speichern(self):

        name = self.name.get().strip()

        if not name:
            messagebox.showwarning(
                "Fehlende Eingabe",
                "Bitte einen Mannschaftsnamen eingeben.",
                parent=self
            )
            return

        daten = {
            "MANNSCHAFT": name,
            "SAISON": self.saison.get(),
            "TYP": self.typ.get()
        }

        if self.team_data:

            dialog = ChangeReasonDialog(
                self,
                title="Mannschaft ändern"
            )

            self.wait_window(dialog)

            if dialog.result is None:
                return

            daten["_GRUND"] = dialog.result["grund"]
            daten["_BEMERKUNG"] = dialog.result["bemerkung"]

            self.service.update_team(
                self.excel_datei,
                self.team_data["TEAM_ID"],
                daten
            )

            self.assignment_service.save_assignments(
                self.excel_datei,
                self.team_data["TEAM_ID"],
                self.get_selected_assignments()
            )

        else:

            self.service.add_team(
                self.excel_datei,
                daten
            )

        if self.on_saved:
            self.on_saved()

        self.destroy()  

    def create_member_tab(self):

        self.assignment = AssignmentWidget(
            self.tab_mitglieder,
            left_title="Verfügbare Mitglieder",
            right_title="Team"
        )

        self.assignment.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

       
        if not self.team_data:
            ctk.CTkLabel(
                self.tab_mitglieder,
                text="Mitglieder können erst nach dem Speichern der Mannschaft zugeordnet werden.",
                font=("Segoe UI", 14)
            ).pack(pady=30)
            return

        roles = self.lookup_service.get_lookup_list(
            self.excel_datei,
            "ROLE"
        )

        self.assignment.set_roles(roles)    

        df = self.member_service.load_members(self.excel_datei)
        df = df.dropna(how="all")

        if "STATUS" in df.columns:
            df = df[
                df["STATUS"].astype(str).str.lower() != "archiviert"
            ]

        assignments = self.assignment_service.load_assignments(
            self.excel_datei,
            self.team_data["TEAM_ID"]
        )

        assigned_ids = set()

        if not assignments.empty:
            assigned_ids = set(
                assignments["MEMBER_ID"].astype(str).tolist()
            )

        left_items = []
        right_items = []

        for _, row in df.iterrows():

            member_id = str(row.get("MEMBER_ID", "")).strip()
            name = f"{row.get('VORNAME', '')} {row.get('NACHNAME', '')}".strip()

            if not member_id or not name:
                continue

            item = {
                "id": member_id,
                "text": name
            }

            if member_id in assigned_ids:
                right_items.append(item)
            else:
                left_items.append(item)

        self.assignment.set_left_items(left_items)
        self.assignment.set_right_items(right_items)
        
    def get_selected_assignments(self):

        assignments = []

        for item in self.assignment.right_items:

            role = item.get("role", "SPIELER")

            role_code = role.upper()
            role_code = role_code.replace("-", "_")
            role_code = role_code.replace(" ", "_")

            assignments.append(
                (
                    item["id"],
                    role_code
                )
            )

        return assignments