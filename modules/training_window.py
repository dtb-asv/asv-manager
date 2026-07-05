import customtkinter as ctk

from modules.team_service import TeamService
from modules.widgets.calendar_entry import CalendarEntry
from modules.training_service import TrainingService
from modules.member_service import MemberService
from modules.lookup_service import LookupService
from modules.training_participant_service import TrainingParticipantService
from modules.widgets.assignment_widget import AssignmentWidget


class TrainingWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        excel_datei,
        on_saved=None,
        training_data=None
    ):

        super().__init__(parent)

        self.excel_datei = excel_datei
        self.on_saved = on_saved
        self.training_data = training_data

        self.service = TrainingService()
        self.team_service = TeamService()

        self.member_service = MemberService()
        self.lookup_service = LookupService()
        self.participant_service = TrainingParticipantService()

        if training_data:
            self.title("Training bearbeiten")
        else:
            self.title("Neues Training")

        self.geometry("720x650")

        self.grab_set()

        titel = "⚽ Neues Training"

        if training_data:
            titel = "✏ Training bearbeiten"

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
        self.tab_teilnehmer = self.tabs.add("Teilnehmer")
        self.tab_history = self.tabs.add("History")

        self.create_general_tab()
        self.create_participant_tab()
        self.load_teams()
        if self.training_data:
            self.fill_data()

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack(pady=20)

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

    def create_general_tab(self):
        ctk.CTkLabel(
            self.tab_allgemein,
            text="Mannschaft"
        ).pack(anchor="w", padx=20)

        self.team = ctk.CTkComboBox(
            self.tab_allgemein,
            values=[],
            width=300
        )
        self.team.pack(
            padx=20,
            pady=(0, 10)
        )

        self.datum = CalendarEntry(
            self.tab_allgemein,
            label_text="Datum"
        )
        self.datum.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Beginn"
        ).pack(anchor="w", padx=20)

        self.startzeit = ctk.CTkEntry(
            self.tab_allgemein,
            placeholder_text="18:00"
        )
        self.startzeit.pack(
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Ende"
        ).pack(anchor="w", padx=20)

        self.endzeit = ctk.CTkEntry(
            self.tab_allgemein,
            placeholder_text="19:30"
        )
        self.endzeit.pack(
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Ort"
        ).pack(anchor="w", padx=20)

        self.ort = ctk.CTkEntry(
            self.tab_allgemein
        )
        self.ort.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            self.tab_allgemein,
            text="Trainingsart"
        ).pack(anchor="w", padx=20)

        self.training_type = ctk.CTkComboBox(
            self.tab_allgemein,
            values=[
                "Training",
                "Torwarttraining",
                "Athletik",
                "Regeneration",
                "Spielvorbereitung"
            ],
            width=300
        )

        self.training_type.pack(
            padx=20,
            pady=(0, 10)
        )

        self.training_type.set("Training")

    def create_participant_tab(self):

        self.assignment = AssignmentWidget(
            self.tab_teilnehmer,
            left_title="Verfügbare Mitglieder",
            right_title="Training"
        )

        self.assignment.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        if not self.training_data:

            ctk.CTkLabel(
                self.tab_teilnehmer,
                text="Teilnehmer können erst nach dem Speichern des Trainings zugeordnet werden.",
                font=("Segoe UI", 14)
            ).pack(pady=30)

            return

        roles = self.lookup_service.get_lookup_list(
            self.excel_datei,
            "ROLE"
        )

        self.assignment.set_roles(roles)

        df = self.member_service.load_members(
            self.excel_datei
        )

        df = df.dropna(how="all")

        if "STATUS" in df.columns:
            df = df[
                df["STATUS"].astype(str).str.lower() != "archiviert"
            ]

        participants = self.participant_service.load_participants(
            self.excel_datei,
            self.training_data["TRAINING_ID"]
        )

        assigned_ids = set()
        participant_roles = {}

        if not participants.empty:

            assigned_ids = set(
                participants["MEMBER_ID"].astype(str).tolist()
            )

            for _, row in participants.iterrows():

                participant_roles[
                    str(row["MEMBER_ID"])
                ] = row.get("ROLE", "SPIELER")

        left_items = []
        right_items = []    
        
        for _, row in df.iterrows():

            member_id = str(row.get("MEMBER_ID", "")).strip()

            name = (
                f"{row.get('VORNAME','')} "
                f"{row.get('NACHNAME','')}"
            ).strip()

            if not member_id or not name:
                continue

            item = {
                "id": member_id,
                "text": name
            }

            if member_id in participant_roles:
                item["role"] = participant_roles[member_id]

            if member_id in assigned_ids:
                right_items.append(item)
            else:
                left_items.append(item)

        self.assignment.set_left_items(left_items)
        self.assignment.set_right_items(right_items)       

    def load_teams(self):

        df = self.team_service.load_teams(
            self.excel_datei
        )

        if df.empty:
            return

        if "AKTIV" in df.columns:
            df = df[
                df["AKTIV"].astype(str).str.upper() == "JA"
            ]

        teams = sorted(
            df["MANNSCHAFT"].dropna().astype(str).tolist()
        )

        self.team.configure(values=teams)

        if teams:
            self.team.set(teams[0])    

    def fill_data(self):

        self.team.set(
            self.training_data.get("TEAM_ID", "")
        )

        self.datum.set(
            self.training_data.get("DATUM", "")
        )

        self.startzeit.insert(
            0,
            str(self.training_data.get("STARTZEIT", ""))
        )

        self.endzeit.insert(
            0,
            str(self.training_data.get("ENDZEIT", ""))
        )

        self.ort.insert(
            0,
            str(self.training_data.get("ORT", ""))
        )

        self.training_type.set(
            self.training_data.get(
                "TRAINING_TYPE",
                "Training"
            )
        )

    def get_selected_participants(self):

        participants = []

        for item in self.assignment.right_items:

            role = item.get("role", "SPIELER")

            role_code = role.upper()
            role_code = role_code.replace("-", "_")
            role_code = role_code.replace(" ", "_")

            participants.append(
                (
                    item["id"],
                    role_code
                )
            )

        return participants    
    
    def speichern(self):

        daten = {
            "TEAM_ID": self.team.get(),
            "DATUM": self.datum.get(),
            "STARTZEIT": self.startzeit.get().strip(),
            "ENDZEIT": self.endzeit.get().strip(),
            "ORT": self.ort.get().strip(),
            "TRAINING_TYPE": self.training_type.get(),
            "STATUS": "Geplant"
        }

        if self.training_data:

            self.service.update_training(
                self.excel_datei,
                self.training_data["TRAINING_ID"],
                daten
            )

            self.participant_service.save_participants(
                self.excel_datei,
                self.training_data["TRAINING_ID"],
                self.get_selected_participants()
            )    

        else:

            training_id = self.service.add_training(
                self.excel_datei,
                daten
            )

            self.participant_service.save_participants(
                self.excel_datei,
                training_id,
                self.get_selected_participants()
            )

        if self.on_saved:
            self.on_saved()

        self.destroy()  