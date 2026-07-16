import customtkinter as ctk

from modules.training_schedules_window import (
    TrainingSchedulesWindow
)


def open_window():

    TrainingSchedulesWindow(
        root,
        excel_datei=r"C:\Users\DTB\ASV-Manager\Excel\Terminefussball_2026_Herbst.xlsx"
    )


root = ctk.CTk()

root.title("Test Trainingspläne")
root.geometry("400x250")

ctk.CTkButton(
    root,
    text="Trainingspläne öffnen",
    command=open_window
).pack(expand=True)

root.mainloop()