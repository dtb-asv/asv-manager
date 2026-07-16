import pandas as pd

from modules.constants import (
    SHEET_TRAINING_SCHEDULES,
    PREFIX_TRAINING_SCHEDULE,
    FIELD_TRAINING_ZONES
)
from modules.id_generator import IdGenerator
from modules.place_service import PlaceService
from modules.team_service import TeamService
from modules.training_schedule_writer import TrainingScheduleWriter


class TrainingScheduleService:

    WEEKDAYS = [
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag"
    ]

    TRAINING_TYPES = [
        "Training",
        "Torwarttraining",
        "Athletik",
        "Regeneration",
        "Spielvorbereitung"
    ]

    def __init__(self):

        self.writer = TrainingScheduleWriter()
        self.place_service = PlaceService()
        self.team_service = TeamService()

    def load_schedules(
        self,
        excel_datei,
        only_active=True
    ):

        df = pd.read_excel(
            excel_datei,
            sheet_name=SHEET_TRAINING_SCHEDULES
        )

        df = df.dropna(how="all")

        if only_active and "AKTIV" in df.columns:

            df = df[
                df["AKTIV"]
                .astype(str)
                .str.strip()
                .str.upper()
                == "JA"
            ]

        return df.reset_index(drop=True)

    def load_schedules_with_names(
        self,
        excel_datei,
        only_active=True
    ):

        schedules = self.load_schedules(
            excel_datei,
            only_active=only_active
        )

        if schedules.empty:
            return schedules

        teams = self.team_service.load_teams(
            excel_datei
        )

        places = self.place_service.load_places_with_facility_name(
            excel_datei
        )

        if not teams.empty:

            team_names = teams[
                [
                    "TEAM_ID",
                    "NAME"
                ]
            ].rename(
                columns={
                    "NAME": "TEAM_NAME"
                }
            )

            schedules = schedules.merge(
                team_names,
                on="TEAM_ID",
                how="left"
            )

        if not places.empty:

            place_names = places[
                [
                    "PLACE_ID",
                    "NAME",
                    "NAME_FACILITY"
                ]
            ].rename(
                columns={
                    "NAME": "PLACE_NAME",
                    "NAME_FACILITY": "FACILITY_NAME"
                }
            )

            schedules = schedules.merge(
                place_names,
                on="PLACE_ID",
                how="left"
            )

        return schedules
    
    def load_schedule(
        self,
        excel_datei,
        schedule_id
    ):

        df = self.load_schedules(
            excel_datei,
            only_active=False
        )

        if df.empty or "SCHEDULE_ID" not in df.columns:
            return None

        result = df[
            df["SCHEDULE_ID"]
            .astype(str)
            .str.strip()
            == str(schedule_id).strip()
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def load_places(self, excel_datei):

        return self.place_service.load_places_with_facility_name(
            excel_datei
        )

    def get_zones_for_place(
        self,
        excel_datei,
        place_id
    ):

        if not place_id:
            return []

        places = self.place_service.load_places(
            excel_datei
        )

        if places.empty:
            return []

        if "PLACE_ID" not in places.columns:
            return []

        result = places[
            places["PLACE_ID"]
            .astype(str)
            .str.strip()
            == str(place_id).strip()
        ]

        if result.empty:
            return []

        zones_value = result.iloc[0].get(
            FIELD_TRAINING_ZONES,
            ""
        )

        if pd.isna(zones_value):
            return []

        zones_text = str(zones_value).strip()

        if not zones_text:
            return []

        zones_text = zones_text.replace(
            ";",
            ","
        )

        zones = [
            zone.strip()
            for zone in zones_text.split(",")
            if zone.strip()
        ]

        return zones

    @staticmethod
    def normalize_time(value):

        if value is None:
            return ""

        if hasattr(value, "strftime"):
            return value.strftime("%H:%M")

        text = str(value).strip()

        if not text or text.lower() == "nan":
            return ""

        if " " in text:
            text = text.split(" ")[-1]

        return text[:5]
    
    def find_schedule_conflicts(
        self,
        excel_datei,
        daten
    ):

        conflicts = []

        schedules = self.load_schedules(
            excel_datei,
            only_active=True
        )

        if schedules.empty:
            return conflicts

        current_schedule_id = str(
            daten.get("SCHEDULE_ID", "")
        ).strip()

        team_id = str(
            daten.get("TEAM_ID", "")
        ).strip()

        weekday = str(
            daten.get("WOCHENTAG", "")
        ).strip()

        place_id = str(
            daten.get("PLACE_ID", "")
        ).strip()

        zone = str(
            daten.get("ZONE", "")
        ).strip()

        start_time = self.normalize_time(
            daten.get("BEGINN", "")
        )

        end_time = self.normalize_time(
            daten.get("ENDE", "")
        )

        for _, row in schedules.iterrows():

            existing_schedule_id = str(
                row.get("SCHEDULE_ID", "")
            ).strip()

            if (
                current_schedule_id
                and existing_schedule_id == current_schedule_id
            ):
                continue

            existing_weekday = str(
                row.get("WOCHENTAG", "")
            ).strip()

            if existing_weekday != weekday:
                continue

            existing_start = self.normalize_time(
                row.get("BEGINN", "")
            )

            existing_end = self.normalize_time(
                row.get("ENDE", "")
            )

            if not (
                start_time < existing_end
                and existing_start < end_time
            ):
                continue

            existing_team_id = str(
                row.get("TEAM_ID", "")
            ).strip()

            existing_place_id = str(
                row.get("PLACE_ID", "")
            ).strip()

            existing_zone = str(
                row.get("ZONE", "")
            ).strip()

            if existing_team_id == team_id:

                conflicts.append(
                    (
                        "Die Mannschaft hat am "
                        f"{weekday} bereits ein Training "
                        f"von {existing_start} bis {existing_end}."
                    )
                )

            if (
                existing_place_id == place_id
                and existing_zone == zone
            ):

                conflicts.append(
                    (
                        f"Der gewählte Platz in Zone {zone} "
                        f"ist am {weekday} bereits von "
                        f"{existing_start} bis {existing_end} belegt."
                    )
                )

        return conflicts
    
    def validate_schedule(self, daten):

        required_fields = {
            "TEAM_ID": "Mannschaft",
            "SAISON": "Saison",
            "WOCHENTAG": "Wochentag",
            "BEGINN": "Beginn",
            "ENDE": "Ende",
            "PLACE_ID": "Platz",
            "ZONE": "Zone",
            "TRAINING_TYPE": "Trainingsart"
        }

        missing = []

        for field, label in required_fields.items():

            value = daten.get(field)

            if value is None or not str(value).strip():
                missing.append(label)

        if missing:

            raise ValueError(
                "Folgende Angaben fehlen: "
                + ", ".join(missing)
            )

        if daten["WOCHENTAG"] not in self.WEEKDAYS:

            raise ValueError(
                "Der gewählte Wochentag ist ungültig."
            )

        if daten["TRAINING_TYPE"] not in self.TRAINING_TYPES:

            raise ValueError(
                "Die gewählte Trainingsart ist ungültig."
            )

        if str(daten["BEGINN"]).strip() >= str(daten["ENDE"]).strip():

            raise ValueError(
                "Die Endzeit muss nach der Beginnzeit liegen."
            )

    def save_schedule(
        self,
        excel_datei,
        daten
    ):

        daten = daten.copy()

        self.validate_schedule(daten)

        schedule_id = daten.get("SCHEDULE_ID")

        if not schedule_id:

            schedule_id = IdGenerator.next_id(
                excel_datei,
                SHEET_TRAINING_SCHEDULES,
                "SCHEDULE_ID",
                PREFIX_TRAINING_SCHEDULE
            )

            daten["SCHEDULE_ID"] = schedule_id
            daten["AKTIV"] = "Ja"

            self.writer.add_schedule(
                excel_datei,
                daten
            )

            return schedule_id

        self.writer.update_schedule(
            excel_datei,
            schedule_id,
            daten
        )

        return schedule_id

    def archive_schedule(
        self,
        excel_datei,
        schedule_id
    ):

        if not schedule_id:

            raise ValueError(
                "Keine SCHEDULE_ID zum Archivieren angegeben."
            )

        self.writer.archive_schedule(
            excel_datei,
            schedule_id
        )