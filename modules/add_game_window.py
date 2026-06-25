import customtkinter as ctk
from tkinter import messagebox
from modules.excel_writer import ExcelWriter


class AddGameWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei, on_saved=None):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.on_saved = on_saved
        self.writer = ExcelWriter()

        self.title("Neues Spiel")
        self.geometry("500x720")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Neues Spiel anlegen",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        self.liga = ctk.CTkEntry(self, placeholder_text="LIGA")
        self.liga.pack(fill="x", padx=20, pady=5)

        self.datum = ctk.CTkEntry(self, placeholder_text="DATUM (TT.MM.JJJJ)")
        self.datum.pack(fill="x", padx=20, pady=5)

        self.startzeit = ctk.CTkEntry(self, placeholder_text="STARTZEIT")
        self.startzeit.pack(fill="x", padx=20, pady=5)

        self.endzeit = ctk.CTkEntry(self, placeholder_text="ENDZEIT")
        self.endzeit.pack(fill="x", padx=20, pady=5)

        self.gegner = ctk.CTkEntry(self, placeholder_text="GEGNER")
        self.gegner.pack(fill="x", padx=20, pady=5)

        self.ort = ctk.CTkEntry(self, placeholder_text="ORT")
        self.ort.pack(fill="x", padx=20, pady=5)

        self.beschreibung = ctk.CTkEntry(self, placeholder_text="BESCHREIBUNG")
        self.beschreibung.pack(fill="x", padx=20, pady=5)

        self.typ = ctk.CTkOptionMenu(self, values=["Heim", "Auswärts"])
        self.typ.pack(fill="x", padx=20, pady=5)

        self.status = ctk.CTkOptionMenu(self, values=["Aktiv", "Abgesagt"])
        self.status.pack(fill="x", padx=20, pady=5)

        self.art = ctk.CTkOptionMenu(
            self,
            values=["Spiel", "Freundschaftsspiel", "Camp"]
        )
        self.art.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(
            self,
            text="Speichern",
            command=self.speichern
        ).pack(pady=25)

    def speichern(self):
        if not self.excel_datei:
            messagebox.showerror("Fehler", "Bitte zuerst eine Excel-Datei auswählen.")
            return

        daten = {
            "LIGA": self.liga.get(),
            "DATUM": self.datum.get(),
            "STARTZEIT": self.startzeit.get(),
            "ENDZEIT": self.endzeit.get(),
            "GEGNER": self.gegner.get(),
            "ORT": self.ort.get(),
            "BESCHREIBUNG": self.beschreibung.get(),
            "TYP": self.typ.get(),
            "STATUS": self.status.get(),
            "ART": self.art.get()
        }

        try:
            backup = self.writer.add_game(self.excel_datei, daten)

            messagebox.showinfo(
                "Gespeichert",
                f"Spiel wurde ins Excel geschrieben.\n\nBackup erstellt:\n{backup}"
            )

            if self.on_saved:
                self.on_saved()

            self.destroy()

        except PermissionError:
            messagebox.showerror(
                "Fehler",
                "Excel-Datei ist vermutlich geöffnet.\nBitte Excel schließen und erneut versuchen."
            )

        except Exception as e:
            messagebox.showerror("Fehler", str(e))