from datetime import date

from modules.training_generator import TrainingGenerator


class TrainingManager:

    def __init__(self):
        self.generator = TrainingGenerator()

    def generate_trainings(
        self,
        schedule: dict,
        start_date: date,
        end_date: date
    ) -> list:

        if not isinstance(schedule, dict):
            raise ValueError(
                "Der Trainingsplan muss ein Dictionary sein."
            )

        if not isinstance(start_date, date):
            raise ValueError(
                "Das Startdatum ist ungültig."
            )

        if not isinstance(end_date, date):
            raise ValueError(
                "Das Enddatum ist ungültig."
            )

        if start_date > end_date:
            raise ValueError(
                "Das Startdatum darf nicht nach dem Enddatum liegen."
            )

        gueltig_ab = schedule.get("GUELTIG_AB")

        if isinstance(gueltig_ab, date):
            effective_start = max(
                start_date,
                gueltig_ab
            )
        else:
            effective_start = start_date

        return self.generator.generate(
            schedule,
            effective_start,
            end_date
        )

    def analyze_generation(
        self,
        schedule: dict,
        start_date: date,
        end_date: date
    ) -> dict:

        trainings = self.generate_trainings(
            schedule,
            start_date,
            end_date
        )

        return {
            "generated": len(trainings),
            "existing": 0,
            "new": len(trainings),
            "warnings": [],
            "trainings": trainings
        }    