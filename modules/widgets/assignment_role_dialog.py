import customtkinter as ctk


class AssignmentRoleDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        item,
        roles
    ):
        super().__init__(parent)

        self.result = None
        self.item = item
        self.roles = roles

        self.title("Rolle auswählen")
        self.geometry("420x260")
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Mitglied zuordnen",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            self,
            text=item["text"],
            font=("Segoe UI", 16)
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self,
            text="Rolle"
        ).pack(anchor="w", padx=40)

        self.role_box = ctk.CTkComboBox(
            self,
            values=roles,
            width=300
        )
        self.role_box.pack(padx=40, pady=(5, 25))

        if roles:
            self.role_box.set(roles[0])

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        buttons.pack(pady=10)

        ctk.CTkButton(
            buttons,
            text="Abbrechen",
            command=self.cancel
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="OK",
            command=self.ok
        ).pack(side="left", padx=10)

    def ok(self):

        self.result = self.role_box.get()
        self.destroy()

    def cancel(self):

        self.result = None
        self.destroy()