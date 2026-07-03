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

        self.scroll = ctk.CTkScrollableFrame(self)

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="❌ Schließen",
            command=self.destroy
        ).pack(pady=15)