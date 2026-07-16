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
        self.minsize(850, 550)
        self.grab_set()

        # ESC schließt das Fenster
        self.bind(
            "<Escape>",
            lambda event: self.destroy()
        )

        # Nur der Tabellenbereich darf mitwachsen
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # =====================================
        # Titel
        # =====================================

        self.title_label = ctk.CTkLabel(
            self,
            text=f"{icon} {title}",
            font=("Segoe UI", 26, "bold")
        )

        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 12)
        )

        # =====================================
        # Suche
        # =====================================

        self.search = SearchBar(
            self,
            callback=search_callback,
            placeholder=search_placeholder
        )

        self.search.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 10)
        )

        # =====================================
        # Toolbar
        # =====================================

        self.toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.toolbar.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 10)
        )

        # =====================================
        # Tabelle
        # =====================================

        self.table = TableView(self)

        # Übergangslösung für alten Code
        self.scroll = self.table

        self.table.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 10)
        )

        # =====================================
        # Footer
        # =====================================

        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.footer.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.status_label = ctk.CTkLabel(
            self.footer,
            text="",
            anchor="w"
        )

        self.status_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.close_button = ctk.CTkButton(
            self.footer,
            text="❌ Schließen",
            width=140,
            command=self.destroy
        )

        self.close_button.pack(
            side="right",
            padx=(10, 0)
        )

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

        self.table.create_header(columns)

    def create_row(self, values, row_data=None):

        self.table.create_row(
            values,
            row_data=row_data
        )

    def get_selected_data(self):

        return self.table.selected_data    

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
                                     