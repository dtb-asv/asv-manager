import customtkinter as ctk
from tkinter import messagebox
from modules.excel_writer import ExcelWriter
from modules.game_service import GameService
from modules.widgets.change_reason_dialog import ChangeReasonDialog


class AddGameWindow(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei, on_saved=None, edit_data=None):
        super().__init__(parent)

        self.excel_datei = excel_datei
        self.on_saved = on_saved
        self.edit_data = edit_data
        self.writer = ExcelWriter()
        self.service = GameService()

        self.is_edit = edit_data is not None

        if self.is_edit:
            self.title("Spiel bearbeiten")
        else:
            self.title("Neues Spiel")

        self.geometry("500x760")
        self.grab_set()

        titel = "Spiel bearbeiten" if self.is_edit else "Neues Spiel anlegen"

        ctk.CTkLabel(
            self,
            text=titel,
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

        if self.is_edit:
            self.fill_fields()

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Speichern",
            command=self.speichern
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="Speichern & schließen",
            command=lambda: self.speichern(close_after=True)
        ).pack(side="left", padx=8)

    def fill_fields(self):
        self.liga.insert(0, str(self.edit_data.get("LIGA", "")))
        self.datum.insert(0, str(self.edit_data.get("DATUM", ""))[:10])
        self.startzeit.insert(0, str(self.edit_data.get("STARTZEIT", ""))[:5])
        self.endzeit.insert(0, str(self.edit_data.get("ENDZEIT", ""))[:5])
        self.gegner.insert(0, str(self.edit_data.get("GEGNER", "")))
        self.ort.insert(0, str(self.edit_data.get("ORT", "")))
        self.beschreibung.insert(0, str(self.edit_data.get("BESCHREIBUNG", "")))

        self.typ.set(str(self.edit_data.get("TYP", "Heim")))
        self.status.set(str(self.edit_data.get("STATUS", "Aktiv")))
        self.art.set(str(self.edit_data.get("ART", "Spiel")))

    def speichern(self, close_after=False):

        if not self.excel_datei:
            messagebox.showerror(
                "Fehler",
                "Bitte zuerst eine Excel-Datei auswählen."
            )
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

            if self.is_edit:

                dialog = ChangeReasonDialog(
                    self,
                    title="Spiel ändern"
                )

                self.wait_window(dialog)

                if dialog.result is None:
                    return

                daten["_GRUND"] = dialog.result["grund"]
                daten["_BEMERKUNG"] = dialog.result["bemerkung"]

                self.service.update_game(
                    self.excel_datei,
                    int(self.edit_data["_EXCEL_ROW"]),
                    daten
                )

            else:

                self.writer.add_game(
                    self.excel_datei,
                    daten
                )

            if self.on_saved:
                self.on_saved()

            if self.is_edit or close_after:

                self.destroy()

            else:

                messagebox.showinfo(
                    "Gespeichert",
                    "Änderungen wurden gespeichert.",
                    parent=self
                )

        except PermissionError:

            messagebox.showerror(
                "Excel geöffnet",
                "Bitte Excel schließen."
            )

        except Exception as e:

            messagebox.showerror(
                "Fehler",
                str(e)
            )