import customtkinter as ctk


class EditWindowBase(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title="Bearbeiten",
        width=900,
        height=700
    ):
        super().__init__(parent)

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.grab_set()

        # ===== Header =====

        self.header = ctk.CTkFrame(self)
        self.header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text=title,
            font=("Segoe UI", 24, "bold")
        )

        self.title_label.pack(anchor="w")

        self.id_label = ctk.CTkLabel(
            self.header,
            text="",
            font=("Segoe UI", 15, "bold"),
            text_color=("gray30", "gray80")
        )

        self.id_label.pack(anchor="w", pady=(5, 0))

        # ===== Tabs =====

        self.tabs = ctk.CTkTabview(self)

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # ===== Footer =====

        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.footer.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.cancel_button = ctk.CTkButton(
            self.footer,
            text="Abbrechen",
            command=self.destroy
        )

        self.cancel_button.pack(
            side="left",
            padx=10
        )

        self.save_button = ctk.CTkButton(
            self.footer,
            text="Speichern",
            command=self.on_save
        )

        self.save_button.pack(
            side="right",
            padx=10
        )

    def add_tab(self, title):

        tab = self.tabs.add(title)

        content = ctk.CTkScrollableFrame(
            tab,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        return content

    def on_save(self):
        pass    

    def show_id(self, text):

        self.id_label.configure(
            text=f"🆔 {text}"
        )      

    def set_title(self, text):

        self.title_label.configure(
            text=text
        )

    def set_save_text(self, text):

        self.save_button.configure(
            text=text
        )        