import customtkinter as ctk

from modules.widgets.date_picker import DatePicker


app = ctk.CTk()
app.title("DatePicker Test")
app.geometry("500x220")

ctk.CTkLabel(
    app,
    text="Datum auswählen",
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=30, pady=(30, 10))

date_picker = DatePicker(app, width=400)
date_picker.pack(fill="x", padx=30)

ctk.CTkButton(
    app,
    text="Ausgabe anzeigen",
    command=lambda: print(date_picker.get(), date_picker.get_date())
).pack(pady=25)

app.mainloop()
