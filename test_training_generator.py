from datetime import date

from modules.training_generator import TrainingGenerator

generator = TrainingGenerator()

schedule = {
    "TEAM_ID": "U10",
    "WOCHENTAG": "Montag",
    "BEGINN": "17:00",
    "ENDE": "18:30",
    "PLACE_ID": "1",
    "ZONE": "A",
    "TRAINING_TYPE": "Training"
}

trainings = generator.generate(
    schedule,
    date(2026, 8, 1),
    date(2026, 8, 31)
)

print(f"{len(trainings)} Trainings erzeugt\n")

for training in trainings:
    print(training)