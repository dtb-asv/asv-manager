import customtkinter as ctk

from modules.widgets.searchable_list import SearchableList


class AssignmentWidget(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        left_title="Verfügbar",
        right_title="Zugeordnet"
    ):

        super().__init__(parent)

        self.left_items = []
        self.right_items = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------- linke Liste ----------

        self.left = SearchableList(
            self,
            left_title,
            on_double_click=self.move_to_right
        )

        self.left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=10
        )

        # ---------- Buttons ----------

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.grid(
            row=0,
            column=1,
            padx=10
        )

        self.btn_add = ctk.CTkButton(
            button_frame,
            text="▶",
            width=45
        )

        self.btn_add.pack(pady=10)

        self.btn_remove = ctk.CTkButton(
            button_frame,
            text="◀",
            width=45
        )

        self.btn_remove.pack(pady=10)

        # ---------- rechte Liste ----------

        self.right = SearchableList(
            self,
            right_title,
            on_double_click=self.move_to_left
        )

        self.right.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

    def set_left_items(self, items):

        self.left_items = items
        self.left.set_items(items)


    def set_right_items(self, items):

        self.right_items = items
        self.right.set_items(items)


    def get_left_selected(self):

        return self.left.get_selected()


    def get_right_selected(self):

        return self.right.get_selected()    

    def move_to_right(self, item):

        if item in self.left_items:
            self.left_items.remove(item)

        if item not in self.right_items:
            self.right_items.append(item)

        self.left.set_items(self.left_items)
        self.right.set_items(self.right_items)


    def move_to_left(self, item):

        if item in self.right_items:
            self.right_items.remove(item)

        if item not in self.left_items:
            self.left_items.append(item)

        self.left.set_items(self.left_items)
        self.right.set_items(self.right_items)    