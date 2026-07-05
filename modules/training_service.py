import pandas as pd

from modules.training_writer import TrainingWriter
from modules.history_service import HistoryService
from modules.id_generator import IdGenerator

from modules.constants import (
    SHEET_TRAININGS,
    PREFIX_TRAINING
)


class TrainingService:

    def __init__(self):

        self.writer = TrainingWriter()
        self.history = HistoryService()

    def load_trainings(self, excel_datei):

        return pd.read_excel(
            excel_datei,
            sheet_name=SHEET_TRAININGS
        )

    def add_training(self, excel_datei, daten):

        training_id = IdGenerator.next_id(
            excel_datei,
            SHEET_TRAININGS,
            "TRAINING_ID",
            PREFIX_TRAINING
        )

        daten["TRAINING_ID"] = training_id
        daten["AKTIV"] = "Ja"

        self.writer.add_training(
            excel_datei,
            daten
        )

        return training_id

    def update_training(
        self,
        excel_datei,
        training_id,
        daten
    ):

        grund = daten.pop("_GRUND", "")
        bemerkung = daten.pop("_BEMERKUNG", "")

        self.writer.update_training(
            excel_datei,
            training_id,
            daten
        )

        objekt = daten.get(
            "DATUM",
            training_id
        )

        self.history.log(
            excel_datei=excel_datei,
            bereich="Training",
            aktion="Bearbeitet",
            objekt=objekt,
            excel_zeile="",
            game_id=training_id,
            grund=grund,
            bemerkung=bemerkung,
            benutzer="System"
        )

    def archive_training(
        self,
        excel_datei,
        training_id
    ):

        self.writer.archive_training(
            excel_datei,
            training_id
        )

        self.history.log(
            excel_datei=excel_datei,
            bereich="Training",
            aktion="Archiviert",
            objekt=training_id,
            excel_zeile="",
            game_id=training_id,
            grund="",
            bemerkung="Training wurde archiviert",
            benutzer="System"
        )