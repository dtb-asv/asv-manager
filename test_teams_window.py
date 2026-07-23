import customtkinter as ctk

from modules.windows.teams_window import TeamsWindow


ctk.set_appearance_mode("dark")


app = ctk.CTk()
app.withdraw()

window = TeamsWindow(app)

# Wenn das Fenster geschlossen wird,
# wird auch die Anwendung beendet.
window.protocol("WM_DELETE_WINDOW", app.destroy)

app.mainloop()