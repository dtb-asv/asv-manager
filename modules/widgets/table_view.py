import customtkinter as ctk


class TableView(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_row = None
        self.selected_data = None
        self.double_click_callback = None

    def clear(self):

        self.selected_row = None
        self.selected_data = None

        for widget in self.winfo_children():
            widget.destroy()

    def refresh(self):

        self.clear()        

    def create_header(self, columns):

        header = ctk.CTkFrame(self)

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
            self,
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

            row.bind(
                "<Double-Button-1>",
                lambda event, r=row_data:
                    self.on_double_click(r)
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
                label.bind(
                    "<Double-Button-1>",
                    lambda event, r=row_data:
                        self.on_double_click(r)
                )

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

    def on_double_click(self, row_data):

        if self.double_click_callback:

            self.double_click_callback(row_data)                           