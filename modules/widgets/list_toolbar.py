import customtkinter as ctk


class ListToolbar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        on_new=None,
        on_edit=None,
        on_archive=None
    ):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkButton(
            self,
            text="➕ Neu",
            command=on_new,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self,
            text="✏ Bearbeiten",
            command=on_edit,
            width=140
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self,
            text="📦 Archivieren",
            command=on_archive,
            width=140
        ).pack(side="left", padx=5)