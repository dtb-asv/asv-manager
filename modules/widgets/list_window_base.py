import customtkinter as ctk

from modules.widgets.search_bar import SearchBar


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

        self.scroll = ctk.CTkScrollableFrame(self)

        self.scroll.pack(
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

        for widget in self.scroll.winfo_children():
            widget.destroy() 

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

    def create_row(self, values):

        row = ctk.CTkFrame(self.scroll)

        row.pack(
            fill="x",
            pady=2
        )

        for value in values:

            ctk.CTkLabel(
                row,
                text=str(value),
                width=180,
                anchor="w"
            ).pack(
                side="left",
                padx=2
            )                       