import customtkinter as ctk

from modules.widgets.selection_dialog import SelectionDialog


app = ctk.CTk()
app.withdraw()

dialog = SelectionDialog(
    app,
    "Spieler auswählen",
        [
        {
            "MEMBER_ID": "MEM000001",
            "TEXT": "Dieter Berger"
        },
        {
            "MEMBER_ID": "MEM000002",
            "TEXT": "Alissia Mottest"
        },
        {
            "MEMBER_ID": "MEM000003",
            "TEXT": "Franz Posposil"
        },
        {
            "MEMBER_ID": "MEM000004",
            "TEXT": "Peter Schwimmer"
        }
    ]
)

result = dialog.show()

print(result["MEMBER_ID"])
print(result["TEXT"])

app.destroy()