import customtkinter as ctk


class SearchBar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        callback=None,
        placeholder="Suchen..."
    ):
        super().__init__(parent)

        self.callback = callback

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="🔍 " + placeholder
        )

        self.entry.pack(
            fill="x",
            expand=True
        )

        self.entry.bind(
            "<KeyRelease>",
            self._changed
        )

    def _changed(self, event):

        if self.callback:
            self.callback(
                self.entry.get()
            )

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, "end")