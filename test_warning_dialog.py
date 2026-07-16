import customtkinter as ctk

from modules.widgets.warning_dialog import WarningDialog


def open_dialog():

    result = WarningDialog.show(
        root,
        "Mögliche Kollisionen gefunden",
        [
            "Die Mannschaft U10 hat am Montag bereits ein Training von 17:00 bis 18:30.",
            "Hauptplatz – Zone A ist am Montag bereits belegt."
        ]
    )

    if result:
        result_label.configure(
            text="Ergebnis: Trotzdem speichern"
        )
    else:
        result_label.configure(
            text="Ergebnis: Abgebrochen"
        )


root = ctk.CTk()

root.title("Test WarningDialog")
root.geometry("450x250")

ctk.CTkButton(
    root,
    text="Warnung öffnen",
    command=open_dialog
).pack(
    pady=(60, 20)
)

result_label = ctk.CTkLabel(
    root,
    text="Noch keine Auswahl"
)

result_label.pack()

root.mainloop()