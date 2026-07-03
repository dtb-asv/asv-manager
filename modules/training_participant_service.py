import pandas as pd
from modules.training_participant_writer import TrainingParticipantWriter
from modules.constants import SHEET_TRAINING_PARTICIPANTS


class TrainingParticipantService:

    def __init__(self):

        self.writer = TrainingParticipantWriter()

    def load_participants(
        self,
        excel_datei,
        training_id
    ):

        df = pd.read_excel(
            excel_datei,
            sheet_name="TRAINING_PARTICIPANTS"
        )

        df = df.dropna(how="all")

        if df.empty:
            return df

        return df[
            df["TRAINING_ID"].astype(str) == str(training_id)
        ]

   def save_participants(
        self,
        excel_datei,
        training_id,
        participants
    ):

        self.writer.deactivate_participants(
            excel_datei,
            training_id
        )

        for member_id, role in participants:

            self.writer.add_participant(
                excel_datei,
                training_id,
                member_id,
                role
            )