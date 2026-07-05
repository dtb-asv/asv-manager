import customtkinter as ctk


class SearchableList(ctk.CTkFrame):

    def __init__(self, parent, title="", on_double_click=None):

        super().__init__(parent)

        self.items = []
        self.selected_item = None
        self.buttons = {}
        self.on_double_click = on_double_click

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.search = ctk.CTkEntry(
            self,
            placeholder_text="Suchen..."
        )

        self.search.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.search.bind(
            "<KeyRelease>",
            lambda e: self.refresh()
        )

        self.list_frame = ctk.CTkScrollableFrame(self)

        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def set_items(self, items):

        self.items = items
        self.refresh()

    def select_item(self, item):

        self.selected_item = item

        for text, button in self.buttons.items():

            if text == item["id"]:
                button.configure(fg_color=("gray70", "gray25"))
            else:
                button.configure(fg_color="transparent")    


    def refresh(self):

        self.buttons = {}

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        text = self.search.get().lower()

        for item in self.items:

            display = item["text"]

            if "role" in item:
                display += f"   [{item['role']}]"

            if text not in display.lower():
                continue

            button = ctk.CTkButton(
                self.list_frame,
                text=display,
                anchor="w",
                fg_color="transparent",
                command=lambda i=item: self.select_item(i)
            )

            button.bind(
                "<Double-Button-1>",
                lambda event, i=item: self.handle_double_click(i)
            )

            button.pack(
                fill="x",
                pady=2
            )

            self.buttons[item["id"]] = button

    def get_selected(self):

        return self.selected_item    

    def handle_double_click(self, item):

        self.select_item(item)

        if self.on_double_click:
            self.on_double_click(item)    