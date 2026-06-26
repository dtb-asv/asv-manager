import customtkinter as ctk


class ArchiveGameWindow(ctk.CTkToplevel):

    def __init__(self, parent, spiel):

        super().__init__(parent)

        self.result = None

        self.title("Spiel archivieren")
        self.geometry("500x450")

        self.grab_set()

        ctk.CTkLabel(
            self,
            text="🗄 Spiel archivieren",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        text = (
            f"{spiel.get('LIGA','')}\n"
            f"{spiel.get('DATUM','')}\n"
            f"{spiel.get('GEGNER','')}"
        )

        ctk.CTkLabel(
            self,
            text=text,
            font=("Segoe UI", 16)
        ).pack(pady=10)

        ctk.CTkLabel(
            self,
            text="Grund"
        ).pack(pady=(20,5))

        self.grund = ctk.CTkOptionMenu(
            self,
            values=[
                "Gegner hat abgesagt",
                "Spiel verlegt",
                "Doppelt angelegt",
                "Fehlerhafte Erfassung",
                "Mannschaft zurückgezogen",
                "Sonstiges"
            ]
        )

        self.grund.pack()

        ctk.CTkLabel(
            self,
            text="Bemerkung"
        ).pack(pady=(20,5))

        self.bemerkung = ctk.CTkTextbox(
            self,
            height=100
        )

        self.bemerkung.pack(
            fill="x",
            padx=20
        )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.destroy
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="Archivieren",
            command=self.ok
        ).pack(
            side="left",
            padx=10
        )

    def ok(self):

        self.result = {
            "grund": self.grund.get(),
            "bemerkung": self.bemerkung.get(
                "1.0",
                "end"
            ).strip()
        }

        self.destroy()