from modules.widgets.list_window_base import ListWindowBase
import customtkinter as ctk
from tkinter import messagebox

from modules.training_service import TrainingService
from modules.training_window import TrainingWindow


class TrainingsWindow(ListWindowBase):

    def __init__(self, parent, excel_datei):

        super().__init__(
            parent,
            title="Trainings",
            icon="🏃",
            search_placeholder="Training suchen...",
            search_callback=self.filter_trainings
        )

        self.service = TrainingService()

        self.selected_training = None
        self.selected_frame = None

        self.parent = parent
        self.excel_datei = excel_datei

       
        ctk.CTkButton(
            self.toolbar,
            text="➕ Neu",
            command=self.neues_training,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.toolbar,
            text="✏ Bearbeiten",
            command=self.bearbeiten_training,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.toolbar,
            text="📦 Archivieren",
            command=self.archivieren_training,
            width=140
        ).pack(side="left", padx=5)

        self.load_trainings()

    def neues_training(self):

        TrainingWindow(
            self,
            self.excel_datei,
            on_saved=self.load_trainings
        )


    def bearbeiten_training(self):

        if self.selected_training is None:
            messagebox.showwarning(
                "Kein Training",
                "Bitte zuerst ein Training auswählen.",
                parent=self
            )
            return

        TrainingWindow(
            self,
            self.excel_datei,
            on_saved=self.load_trainings,
            training_data=self.selected_training
        )


    def archivieren_training(self):

        if self.selected_training is None:
            messagebox.showwarning(
                "Kein Training",
                "Bitte zuerst ein Training auswählen.",
                parent=self
            )
            return

        antwort = messagebox.askyesno(
            "Training archivieren",
            f"Soll das Training vom {self.selected_training['DATUM']} archiviert werden?",
            parent=self
        )

        if not antwort:
            return

        self.service.archive_training(
            self.excel_datei,
            self.selected_training["TRAINING_ID"]
        )

        self.load_trainings()


    def filter_trainings(self, text):

        text = text.strip().lower()

        if text == "":
            self.load_trainings()
            return

        df = self.df.copy()

        mask = (
            df["DATUM"].astype(str).str.lower().str.contains(text)
            |
            df["TEAM_ID"].astype(str).str.lower().str.contains(text)
            |
            df["ORT"].astype(str).str.lower().str.contains(text)
            |
            df["TRAINING_ID"].astype(str).str.lower().str.contains(text)
        )

        self.draw_trainings(df[mask]) 

    def load_trainings(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.selected_training = None
        self.selected_frame = None

        df = self.service.load_trainings(
            self.excel_datei
        )

        df = df.dropna(how="all")

        if "AKTIV" in df.columns:
            df = df[
                df["AKTIV"].astype(str).str.lower() == "ja"
            ]

        if df.empty:

            ctk.CTkLabel(
                self.scroll,
                text="Noch keine Trainings vorhanden.",
                font=("Segoe UI", 15)
            ).pack(pady=20)

            return

        self.df = df.copy()

        self.draw_trainings(df)    

    def draw_trainings(self, df):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        columns = [
            "TRAINING_ID",
            "DATUM",
            "STARTZEIT",
            "TEAM_ID"
        ]

        header = ctk.CTkFrame(self.scroll)
        header.pack(fill="x")

        for col in columns:

            ctk.CTkLabel(
                header,
                text=col,
                width=180,
                font=("Segoe UI", 13, "bold")
            ).pack(side="left", padx=3)

        for _, row in df.iterrows():

            frame = ctk.CTkFrame(
                self.scroll,
                fg_color="transparent"
            )

            frame.pack(fill="x", pady=2)

            row_data = row.to_dict()

            frame.bind(
                "<Button-1>",
                lambda event, r=row_data, f=frame:
                    self.select_training(r, f)
            )

            frame.bind(
                "<Double-Button-1>",
                lambda event:
                    self.bearbeiten_training()
            )

            for col in columns:

                label = ctk.CTkLabel(
                    frame,
                    text=str(row.get(col, "")),
                    width=180
                )

                label.pack(side="left", padx=3)

                label.bind(
                    "<Button-1>",
                    lambda event, r=row_data, f=frame:
                        self.select_training(r, f)
                )

                label.bind(
                    "<Double-Button-1>",
                    lambda event:
                        self.bearbeiten_training()
                ) 

    def select_training(self, row, frame):

        if self.selected_frame:
            self.selected_frame.configure(
                fg_color="transparent"
            )

        frame.configure(
            fg_color=("lightblue", "#1F538D")
        )

        self.selected_frame = frame
        self.selected_training = row               