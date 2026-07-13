import customtkinter as ctk

from modules.widgets.search_bar import SearchBar
from modules.widgets.table_view import TableView


class ListWindowBase(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title,
        icon,
        search_placeholder,
        search_callback
    ):
        super().__init__(parent)

        self.title(title)
        self.geometry("1000x650")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text=f"{icon} {title}",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

        self.toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.toolbar.pack(pady=5)

        self.search = SearchBar(
            self,
            callback=search_callback,
            placeholder=search_placeholder
        )

        self.search.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.toolbar.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.table = TableView(self)

        self.scroll = self.table

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w"
        )

        self.status_label.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkButton(
            self,
            text="❌ Schließen",
            command=self.destroy
        ).pack(pady=15)

        self.selected_row = None

    def add_toolbar_button(
        self,
        text,
        command
    ):

        ctk.CTkButton(
            self.toolbar,
            text=text,
            width=120,
            command=command
        ).pack(
            side="left",
            padx=(0, 10)
        )    

    def clear_scroll(self):

        self.table.clear()

    def set_status(self, text):

        self.status_label.configure(text=text)

    def create_header(self, columns):

        header = ctk.CTkFrame(self.scroll)

        header.pack(
            fill="x",
            pady=(0, 4)
        )

        for column in columns:

            ctk.CTkLabel(
                header,
                text=column,
                width=180,
                anchor="w",
                font=("Segoe UI", 13, "bold")
            ).pack(
                side="left",
                padx=2
            )

    def create_row(self, values, row_data=None):

        row = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            pady=2
        )

        if row_data is not None:

            row.bind(
                "<Button-1>",
                lambda event, f=row, r=row_data:
                    self.select_row(f, r)
            )

        for value in values:

            label = ctk.CTkLabel(
                row,
                text=str(value),
                width=180,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=2
            )

            if row_data is not None:

                label.bind(
                    "<Button-1>",
                    lambda event, f=row, r=row_data:
                        self.select_row(f, r)
                )
    def refresh(self):

        self.clear_scroll()
        self.load_data()

    def select_row(self, frame, row_data):

        if self.selected_row and self.selected_row.winfo_exists():

            self.selected_row.configure(
                fg_color="transparent"
            )

        frame.configure(
            fg_color=("royalblue", "royalblue4")
        )

        self.selected_row = frame
        self.selected_data = row_data     

    def create_table(self, dataframe, columns):

        self.create_header(columns)

        for _, row in dataframe.iterrows():

            values = [
                row.get(col, "")
                for col in columns
            ]

            self.create_row(values)                                