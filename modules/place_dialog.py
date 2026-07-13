import customtkinter as ctk
from modules.facility_service import FacilityService


class PlaceDialog(ctk.CTkToplevel):

    def __init__(self, parent, excel_datei, title, daten=None):

        super().__init__(parent)

        self.service = FacilityService()

        df = self.service.load_facilities(excel_datei)

        facility_names = df["NAME"].tolist()

        self.facility_map = dict(
            zip(
                df["NAME"],
                df["FACILITY_ID"]
            )
        )

        if not facility_names:
            facility_names = ["Keine Sportanlage vorhanden"]

        self.result = None

        self.title(title)
        self.geometry("420x220")
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
            text="Sportanlage",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.facility_combo = ctk.CTkComboBox(
            self,
            values=facility_names
        )

        self.facility_combo.pack(
            padx=20,
            fill="x"
        )

        if facility_names:
            self.facility_combo.set(facility_names[0])

        if daten:
            self.name_entry.insert(
                0,
                daten.get("NAME", "")
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

        facility_name = self.facility_combo.get()

        self.result = {
            "NAME": name,
            "FACILITY_ID": self.facility_map.get(facility_name, "")
        }

        self.destroy()    

    def show(self):

        self.wait_window()

        return self.result    