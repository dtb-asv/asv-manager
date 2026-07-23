import customtkinter as ctk


class FacilityDialog(ctk.CTkToplevel):

    def __init__(self, parent, title, daten=None):

        super().__init__(parent)

        self.result = None

        self.title(title)
        self.geometry("420x300")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Name",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.name_entry = ctk.CTkEntry(
            self,
            width=360
        )
        self.name_entry.pack(
            padx=20,
            fill="x"
        )
        ctk.CTkLabel(
            self,
            text="Adresse",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.address_entry = ctk.CTkEntry(
            self,
            width=360
        )

        self.address_entry.pack(
            padx=20,
            fill="x"
        )

        if daten:

            self.name_entry.insert(
                0,
                daten.get(
                    "name",
                    daten.get("NAME", "")
                )
            )

            self.address_entry.insert(
                0,
                daten.get(
                    "address",
                    daten.get("ADDRESS", "")
                )
            )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack(
            pady=25
        )

        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.destroy
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="Speichern",
            command=self.save
        ).pack(
            side="left",
            padx=10
        )

    def save(self):

        name = self.name_entry.get().strip()

        if not name:
            return

        self.result = {
            "name": name,
            "address": self.address_entry.get().strip()
        }

        self.destroy()    

    def show(self):

        self.wait_window()

        return self.result    