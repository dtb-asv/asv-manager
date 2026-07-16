import customtkinter as ctk
from modules.team_service import TeamService
from tkinter import messagebox
from modules.widgets.change_reason_dialog import ChangeReasonDialog
from modules.member_service import MemberService
from modules.lookup_service import LookupService
from modules.team_assignment_service import TeamAssignmentService
from modules.widgets.assignment_widget import AssignmentWidget
from modules.department_service import DepartmentService
from modules.widgets.table_view import TableView
from modules.widgets.selection_dialog import SelectionDialog
from modules.team_member_service import TeamMemberService
from modules.member_window import MemberWindow


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
        self.department_service = DepartmentService()

        df = self.department_service.load_departments(excel_datei)

        department_names = df["NAME"].tolist()

        self.department_map = dict(
            zip(
                df["NAME"],
                df["DEPARTMENT_ID"]
            )
        )


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

        self.bind(
            "<Escape>",
            lambda event: self.destroy()
        )

        self.bind(
            "<Return>",
            lambda event: self.speichern()
        )

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
        self.tab_spieler = self.tabs.add("Spieler")
        self.tab_trainer = self.tabs.add("Trainer")
        self.tab_training = self.tabs.add("Training")
        self.tab_vereine = self.tabs.add("Vereine")
        self.tab_history = self.tabs.add("History")

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Mannschaft"
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Bereich"
        ).pack(anchor="w", padx=20)

        self.department = ctk.CTkComboBox(
            self.tab_allgemein,
            width=300,
            values=department_names
        )

        self.department.pack(
            padx=20,
            pady=(0, 10)
        )

        if department_names:
            self.department.set(department_names[0])
        
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
            text="Altersklasse"
        ).pack(anchor="w", padx=20)

        self.altersklasse = ctk.CTkComboBox(
            self.tab_allgemein,
            width=300,
            values=[
                "FK",
                "U6",
                "U7",
                "U8",
                "U9",
                "U10",
                "U11",
                "U12",
                "U13",
                "U14",
                "U15",
                "U16",
                "KM",
                "Reserve",
                "Frauen",
                "Mädchen"
            ]
        )

        self.altersklasse.pack(
            padx=20,
            pady=(0, 20)
        )

        self.altersklasse.set("FK")

        if self.team_data:

            self.name.insert(
                0,
                self.team_data.get("NAME", "")
            )

            self.saison.set(
                self.team_data.get("SAISON", "2026/2027")
            )

            self.altersklasse.set(
                self.team_data.get("ALTERSKLASSE", "Normal")
            )
        
        self.create_player_tab()
        self.create_trainer_tab()

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        save_text = "Mannschaft anlegen"

        if self.team_data:
            save_text = "Änderungen speichern"

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            width=120,
            command=self.destroy
        ).pack(
            side="right",
            padx=(10, 0)
        )

        ctk.CTkButton(
            button_frame,
            text=save_text,
            width=120,
            command=self.speichern
        ).pack(
            side="right"
        )

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
            "NAME": name,
            "ALTERSKLASSE": self.altersklasse.get(),
            "DEPARTMENT_ID": self.department_map.get(
                self.department.get(),
                ""
            )
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

    def create_player_tab(self):

        header = ctk.CTkFrame(
            self.tab_spieler,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            header,
            text="Spieler der Mannschaft",
            font=("Segoe UI", 18, "bold")
        ).pack(
            side="left"
        )

        self.player_count = ctk.CTkLabel(
            self.tab_spieler,
            text="",
            font=("Segoe UI", 12)
        )

        self.player_count.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        button_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        button_frame.pack(
            side="right"
        )

        ctk.CTkButton(
            button_frame,
            text="➖ Spieler entfernen",
            width=140,
            command=self.remove_player
        ).pack(
            side="right",
            padx=(5,0)
        )

        ctk.CTkButton(
            button_frame,
            text="➕ Spieler hinzufügen",
            width=140,
            command=self.add_player
        ).pack(
            side="right"
        )

        self.player_table = TableView(
            self.tab_spieler
        )

        self.player_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0,20)
        )

        self.player_table.double_click_callback = (
            self.open_player
        )

        self.player_table.create_header(
            [
                "Vorname",
                "Nachname"
            ]
        )
        self.load_team_players()

    def add_player(self):

        service = TeamMemberService()

        df = service.get_all_players(
            self.excel_datei
        )

        values = [
            {
                "MEMBER_ID": row["MEMBER_ID"],
                "TEXT": f"{row['VORNAME']} {row['NACHNAME']}"
            }
            for _, row in df.iterrows()
        ]

        dialog = SelectionDialog(
            self,
            "Spieler auswählen",
            values
        )

        result = dialog.show()

        if result:

            if not self.team_data:
                messagebox.showwarning(
                    "Mannschaft noch nicht gespeichert",
                    "Bitte die Mannschaft zuerst speichern, bevor Spieler zugeordnet werden.",
                    parent=self
                )
                return

            success = service.assign_player(
                self.excel_datei,
                self.team_data["TEAM_ID"],
                result["MEMBER_ID"]
            )

            self.load_team_players()
            
            if success:
                messagebox.showinfo(
                    "Spieler zugeordnet",
                    f"{result['TEXT']} wurde der Mannschaft zugeordnet.",
                    parent=self
                )
            else:
                messagebox.showinfo(
                    "Bereits zugeordnet",
                    f"{result['TEXT']} ist bereits als Spieler in dieser Mannschaft eingetragen.",
                    parent=self
                )

    def load_team_players(self):

        self.player_table.clear()

        self.player_table.create_header(
            [
                "Vorname",
                "Nachname"
            ]
        )

        if not self.team_data:
            return

        service = TeamMemberService()

        df = service.get_team_players(
            self.excel_datei,
            self.team_data["TEAM_ID"]
        )

        count = len(df)

        if count == 0:

            self.player_count.configure(
                text="Keine Spieler vorhanden"
            )

        elif count == 1:

            self.player_count.configure(
                text="1 Spieler"
            )

        else:

            self.player_count.configure(
                text=f"{count} Spieler"
            )

        for _, row in df.iterrows():

            self.player_table.create_row(
                [
                    row["VORNAME"],
                    row["NACHNAME"]
                ],
                row_data=row.to_dict()
            )  

    def remove_player(self):

        selected = self.player_table.selected_data

        if selected is None:

            messagebox.showwarning(
                "Kein Spieler",
                "Bitte zuerst einen Spieler auswählen.",
                parent=self
            )

            return

        if not messagebox.askyesno(
            "Spieler entfernen",
            f"Soll '{selected['VORNAME']} {selected['NACHNAME']}' "
            "aus der Mannschaft entfernt werden?",
            parent=self
        ):
            return

        service = TeamMemberService()

        success = service.remove_player(
            self.excel_datei,
            selected["TEAM_MEMBER_ID"]
        )

        if success:

            self.load_team_players()

            messagebox.showinfo(
                "Spieler entfernt",
                "Der Spieler wurde aus der Mannschaft entfernt.",
                parent=self
            )

    def open_player(self, player_data):

        MemberWindow(
            self,
            on_saved=self.load_team_players,
            member_data=player_data
        ) 

    def create_trainer_tab(self):

        header = ctk.CTkFrame(
            self.tab_trainer,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            header,
            text="Trainerteam",
            font=("Segoe UI", 18, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            header,
            text="➕ Trainer hinzufügen",
            width=160,
            command=self.add_trainer
        ).pack(
            side="right"
        )

        self.trainer_table = TableView(
            self.tab_trainer
        )

        self.trainer_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )
        self.trainer_table.double_click_callback = (
            self.open_player
        )

        self.trainer_table.create_header(
            [
                "Vorname",
                "Nachname",
                "Funktion"
            ]
        )
        self.load_team_staff()

    def load_team_staff(self):

        self.trainer_table.clear()

        self.trainer_table.create_header(
            [
                "Vorname",
                "Nachname",
                "Funktion"
            ]
        )

        if not self.team_data:
            return

        service = TeamMemberService()

        df = service.get_team_staff(
            self.excel_datei,
            self.team_data["TEAM_ID"]
        )

        for _, row in df.iterrows():

            self.trainer_table.create_row(
                [
                    row["VORNAME"],
                    row["NACHNAME"],
                    row["ROLLE"]
                ],
                row_data=row.to_dict()
            )    

    def add_trainer(self):

        service = TeamMemberService()

        df = service.get_all_staff(
            self.excel_datei
        )

        values = [
            {
                "MEMBER_ID": row["MEMBER_ID"],
                "ROLE_CODE": row["ROLE_CODE"],
                "TEXT": (
                    f"{row['VORNAME']} "
                    f"{row['NACHNAME']} "
                    f"({row['ROLE_CODE']})"
                )
            }
            for _, row in df.iterrows()
        ]

        dialog = SelectionDialog(
            self,
            "Trainer auswählen",
            values
        )

        result = dialog.show()

        if result:

            if not self.team_data:
                messagebox.showwarning(
                    "Mannschaft noch nicht gespeichert",
                    "Bitte die Mannschaft zuerst speichern, bevor Trainer zugeordnet werden.",
                    parent=self
                )
                return

            success = service.assign_staff(
                self.excel_datei,
                self.team_data["TEAM_ID"],
                result["MEMBER_ID"],
                result["ROLE_CODE"]
            )

            if success:
                self.load_team_staff()
                messagebox.showinfo(
                    "Trainerteam ergänzt",
                    f"{result['TEXT']} wurde der Mannschaft zugeordnet.",
                    parent=self
                )
            else:
                messagebox.showinfo(
                    "Bereits zugeordnet",
                    f"{result['TEXT']} ist bereits mit dieser Funktion eingetragen.",
                    parent=self
                )           