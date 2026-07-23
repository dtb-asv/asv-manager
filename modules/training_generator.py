from datetime import date, timedelta


class TrainingGenerator:

    WEEKDAY_MAP = {
        "Montag": 0,
        "Dienstag": 1,
        "Mittwoch": 2,
        "Donnerstag": 3,
        "Freitag": 4,
        "Samstag": 5,
        "Sonntag": 6,
    }

    def generate(
        self,
        schedule: dict,
        start_date: date,
        end_date: date
    ) -> list:

        matching_dates = self._get_matching_dates(
            schedule["WOCHENTAG"],
            start_date,
            end_date
        )

        trainings = []

        for training_date in matching_dates:
            trainings.append(
                self._create_training(
                    schedule,
                    training_date
                )
            )

        return trainings

    def _get_matching_dates(
        self,
        weekday_name: str,
        start_date: date,
        end_date: date
    ) -> list:

        weekday = self.WEEKDAY_MAP[weekday_name]

        result = []

        current = start_date

        while current <= end_date:

            if current.weekday() == weekday:
                result.append(current)

            current += timedelta(days=1)

        return result

    def _create_training(
        self,
        schedule: dict,
        training_date: date
    ) -> dict:

        return {
            "TEAM_ID": schedule["TEAM_ID"],
            "DATUM": training_date,
            "STARTZEIT": schedule["BEGINN"],
            "ENDZEIT": schedule["ENDE"],
            "PLACE_ID": schedule["PLACE_ID"],
            "ZONE": schedule["ZONE"],
            "TRAINING_TYPE": schedule["TRAINING_TYPE"],
            "STATUS": "Geplant",
            "AKTIV": "Ja",
            "BEMERKUNG": ""
        }