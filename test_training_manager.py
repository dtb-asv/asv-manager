from datetime import date

from modules.managers.training_manager import TrainingManager


manager = TrainingManager()

schedule = {
    "TEAM_ID": "U10",
    "GUELTIG_AB": date(2026, 8, 12),
    "WOCHENTAG": "Montag",
    "BEGINN": "17:00",
    "ENDE": "18:30",
    "PLACE_ID": "1",
    "ZONE": "A",
    "TRAINING_TYPE": "Training"
}

trainings = manager.generate_trainings(
    schedule,
    date(2026, 8, 1),
    date(2026, 8, 31)
)

print(f"{len(trainings)} Trainings erzeugt")

for training in trainings:
    print(training["DATUM"])