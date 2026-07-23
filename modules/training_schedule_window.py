import customtkinter as ctk
from modules.team_service import TeamService
from modules.place_service import PlaceService
from modules.training_schedule_service import TrainingScheduleService
from modules.widgets.warning_dialog import WarningDialog
from modules.widgets.date_picker import DatePicker


class TrainingScheduleWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        excel_datei,
        on_saved=None,
        schedule_data=None
    ):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.on_saved = on_saved
        self.schedule_data = schedule_data
        self.service = TrainingScheduleService()

        self.team_service = TeamService()
        self.place_service = PlaceService()

        self.team_map = {}
        self.place_map = {}    

        if self.schedule_data:
            self.title("Trainingsplan bearbeiten")
        else:
            self.title("Neuer Trainingsplan")

        self.geometry("650x650")
        self.minsize(600, 550)

        self.transient(parent)
        self.grab_set()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel
        )

        self.bind(
            "<Escape>",
            lambda event: self.cancel()
        )

        self.create_widgets()

        self.load_teams()
        self.load_places()

        if self.schedule_data:
            self.load_data()

    def create_widgets(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # -----------------------------
        # Kopfbereich
        # -----------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        if self.schedule_data:
            title_text = "✏ Trainingsplan bearbeiten"
        else:
            title_text = "📅 Neuer Trainingsplan"

        ctk.CTkLabel(
            header,
            text=title_text,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Wiederkehrenden Saison-Trainingsplan verwalten",
            font=("Segoe UI", 13),
            text_color=("gray40", "gray70")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # -----------------------------
        # Inhaltsbereich
        # -----------------------------

        self.content_frame = ctk.CTkScrollableFrame(
            self
        )
        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=10
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Mannschaft"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 5)
        )

        self.team_combo = ctk.CTkComboBox(
            self.content_frame,
            values=[],
            width=400
        )
        self.team_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Platz"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.place_combo = ctk.CTkComboBox(
            self.content_frame,
            values=[],
            width=400,
            command=self.on_place_changed
        )
        self.place_combo.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Zone"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.zone_combo = ctk.CTkComboBox(
            self.content_frame,
            values=[],
            width=400
        )
        self.zone_combo.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Saison"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.saison_combo = ctk.CTkComboBox(
            self.content_frame,
            values=[
                "2025/2026",
                "2026/2027",
                "2027/2028",
                "2028/2029"
            ],
            width=400
        )

        self.saison_combo.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.saison_combo.set("2026/2027")

        ctk.CTkLabel(
            self.content_frame,
            text="Gültig ab"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.gueltig_ab_picker = DatePicker(
            self.content_frame,
            width=400
        )

        self.gueltig_ab_picker.grid(
            row=9,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Wochentag"
        ).grid(
            row=10,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.weekday_combo = ctk.CTkComboBox(
            self.content_frame,
            values=self.service.WEEKDAYS,
            width=400
        )

        self.weekday_combo.grid(
            row=11,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.weekday_combo.set("Montag")

        time_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )

        time_frame.grid(
            row=12,
            column=0,
            sticky="ew",
            padx=20,
            pady=(5, 15)
        )

        time_frame.grid_columnconfigure(0, weight=1)
        time_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            time_frame,
            text="Beginn"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=(0, 5)
        )

        ctk.CTkLabel(
            time_frame,
            text="Ende"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(10, 0),
            pady=(0, 5)
        )

        self.start_entry = ctk.CTkEntry(
            time_frame,
            placeholder_text="17:00"
        )

        self.start_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.end_entry = ctk.CTkEntry(
            time_frame,
            placeholder_text="18:30"
        )

        self.end_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0)
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Trainingsart"
        ).grid(
            row=13,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.training_type_combo = ctk.CTkComboBox(
            self.content_frame,
            values=self.service.TRAINING_TYPES,
            width=400
        )

        self.training_type_combo.grid(
            row=14,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.training_type_combo.set("Training")

        ctk.CTkLabel(
            self.content_frame,
            text="Bemerkung"
        ).grid(
            row=15,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 5)
        )

        self.remark_textbox = ctk.CTkTextbox(
            self.content_frame,
            height=100
        )

        self.remark_textbox.grid(
            row=16,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20)
        )

        # -----------------------------
        # Fußbereich
        # -----------------------------

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 20)
        )

        footer.grid_columnconfigure(0, weight=1)

        button_frame = ctk.CTkFrame(
            footer,
            fg_color="transparent"
        )
        button_frame.grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            width=120,
            command=self.cancel
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Speichern",
            width=120,
            command=self.save
        )
        self.save_button.pack(side="left")

    def load_data(self):

        team_id = str(
            self.schedule_data.get("TEAM_ID", "")
        ).strip()

        for team_name, mapped_team_id in self.team_map.items():

            if str(mapped_team_id).strip() == team_id:
                self.team_combo.set(team_name)
                break

        self.saison_combo.set(
            str(
                self.schedule_data.get(
                    "SAISON",
                    "2026/2027"
                )
            ).strip()
        )

        gueltig_ab = str(
            self.schedule_data.get(
                "GUELTIG_AB",
                ""
            )
        ).strip()

        if gueltig_ab:
            self.gueltig_ab_picker.set_date(gueltig_ab)

        self.weekday_combo.set(
            str(
                self.schedule_data.get(
                    "WOCHENTAG",
                    "Montag"
                )
            ).strip()
        )

        self.start_entry.delete(0, "end")
        self.start_entry.insert(
            0,
            str(
                self.schedule_data.get(
                    "BEGINN",
                    ""
                )
            ).strip()
        )

        self.end_entry.delete(0, "end")
        self.end_entry.insert(
            0,
            str(
                self.schedule_data.get(
                    "ENDE",
                    ""
                )
            ).strip()
        )

        self.training_type_combo.set(
            str(
                self.schedule_data.get(
                    "TRAINING_TYPE",
                    "Training"
                )
            ).strip()
        )

        place_id = str(
            self.schedule_data.get(
                "PLACE_ID",
                ""
            )
        ).strip()

        selected_place_name = ""

        for place_name, mapped_place_id in self.place_map.items():

            if str(mapped_place_id).strip() == place_id:
                selected_place_name = place_name
                self.place_combo.set(place_name)
                break

        if selected_place_name:

            self.on_place_changed(
                selected_place_name
            )

        zone = str(
            self.schedule_data.get(
                "ZONE",
                ""
            )
        ).strip()

        if zone:
            self.zone_combo.set(zone)

        self.remark_textbox.delete(
            "1.0",
            "end"
        )

        bemerkung = str(
            self.schedule_data.get(
                "BEMERKUNG",
                ""
            )
        ).strip()

        if bemerkung:
            self.remark_textbox.insert(
                "1.0",
                bemerkung
            )    
    
    def on_place_changed(self, selected_place=None):

        if selected_place is None:
            selected_place = self.place_combo.get()

        place_id = self.place_map.get(
            selected_place,
            ""
        )

        zones = self.service.get_zones_for_place(
            self.excel_datei,
            place_id
        )

        self.zone_combo.configure(
            values=zones
        )

        if zones:
            self.zone_combo.set(zones[0])
        else:
            self.zone_combo.set("")
    
    def load_teams(self):

        df = self.team_service.load_teams(
            self.excel_datei
        )

        if df.empty:
            return

        if "AKTIV" in df.columns:

            df = df[
                df["AKTIV"]
                .astype(str)
                .str.strip()
                .str.upper()
                == "JA"
            ]

        team_names = []

        self.team_map.clear()

        for _, row in df.iterrows():

            team_name = str(
                row.get("NAME", "")
            ).strip()

            team_id = str(
                row.get("TEAM_ID", "")
            ).strip()

            if not team_name or not team_id:
                continue

            team_names.append(team_name)
            self.team_map[team_name] = team_id

        self.team_combo.configure(
            values=team_names
        )

        if team_names:
            self.team_combo.set(
                team_names[0]
            )

    def load_places(self):

        df = self.place_service.load_places_with_facility_name(
            self.excel_datei
        )

        if df.empty:
            return

        place_names = []

        self.place_map.clear()

        for _, row in df.iterrows():

            place_name = str(
                row.get("NAME", "")
            ).strip()

            facility_name = str(
                row.get("NAME_FACILITY", "")
            ).strip()

            place_id = str(
                row.get("PLACE_ID", "")
            ).strip()

            if not place_name or not place_id:
                continue

            if facility_name:
                display_text = (
                    f"{place_name} ({facility_name})"
                )
            else:
                display_text = place_name

            place_names.append(display_text)
            self.place_map[display_text] = place_id

        self.place_combo.configure(
            values=place_names
        )

        if place_names:
            self.place_combo.set(
                place_names[0]
            )

            self.on_place_changed(
                place_names[0]
            )     

    def collect_data(self):

        selected_team = self.team_combo.get()
        selected_place = self.place_combo.get()

        return {
            "SCHEDULE_ID": (
                self.schedule_data.get("SCHEDULE_ID", "")
                if self.schedule_data
                else ""
            ),
            "TEAM_ID": self.team_map.get(
                selected_team,
                ""
            ),
            "SAISON": self.saison_combo.get().strip(),
            "GUELTIG_AB": self.gueltig_ab_picker.get_date(),
            "WOCHENTAG": self.weekday_combo.get().strip(),
            "BEGINN": self.start_entry.get().strip(),
            "ENDE": self.end_entry.get().strip(),
            "PLACE_ID": self.place_map.get(
                selected_place,
                ""
            ),
            "ZONE": self.zone_combo.get().strip(),
            "TRAINING_TYPE": (
                self.training_type_combo.get().strip()
            ),
            "AKTIV": (
                self.schedule_data.get("AKTIV", "Ja")
                if self.schedule_data
                else "Ja"
            ),
            "BEMERKUNG": (
                self.remark_textbox
                .get("1.0", "end")
                .strip()
            )
        }
    
    def save(self):

        daten = self.collect_data()

        try:

            self.service.validate_schedule(
                daten
            )

            conflicts = self.service.find_schedule_conflicts(
                self.excel_datei,
                daten
            )

            if conflicts:

                confirmed = WarningDialog.show(
                    self,
                    "Mögliche Kollisionen gefunden",
                    conflicts
                )

                if not confirmed:
                    return

            self.service.save_schedule(
                self.excel_datei,
                daten
            )

        except ValueError as error:

            from tkinter import messagebox

            messagebox.showwarning(
                "Eingaben prüfen",
                str(error),
                parent=self
            )

            return

        except Exception as error:

            from tkinter import messagebox

            messagebox.showerror(
                "Fehler beim Speichern",
                str(error),
                parent=self
            )

            return

        if self.on_saved:
            self.on_saved()

        self.destroy()

    def cancel(self):

        self.destroy()