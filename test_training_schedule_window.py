import customtkinter as ctk

from modules.training_schedule_window import TrainingScheduleWindow


def open_window():

              
    TrainingScheduleWindow(
        root,
        excel_datei=r"C:\Users\DTB\ASV-Manager\Excel\Terminefussball_2026_Herbst.xlsx",
    )
          

root = ctk.CTk()

root.title("Test Trainingsplan")
root.geometry("400x250")

ctk.CTkButton(
    root,
    text="Trainingsplan öffnen",
    command=open_window
).pack(
    expand=True
)

root.mainloop()