import customtkinter as ctk
from modules.widgets.table_view import TableView


class SelectionDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title,
        values
    ):
        super().__init__(parent)

        self.title(title)
        self.geometry("500x600")
        self.grab_set()

        self.result = None
        self.values = values

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

        self.search = ctk.CTkEntry(
            self,
            placeholder_text="Suchen..."
        )

        self.search.pack(
            fill="x",
            padx=20
        )

        self.table = TableView(self)

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        self.table.create_header([
            "Auswahl"
        ])

        for item in values:

            self.table.create_row(
                [
                    item["TEXT"]
                ],
                row_data=item
            )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.destroy
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            button_frame,
            text="Übernehmen",
            command=self.uebernehmen
        ).pack(
            side="right"
        )

    def uebernehmen(self):

        selected = self.table.selected_data

        if selected is None:
            return

        self.result = selected

        self.destroy()

    def show(self):

        self.wait_window()

        return self.result       