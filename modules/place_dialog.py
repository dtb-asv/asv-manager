import customtkinter as ctk
import pandas as pd
from modules.facility_service import FacilityService


class PlaceDialog(ctk.CTkToplevel):

    def __init__(self, parent, title, daten=None):

        super().__init__(parent)

        self.service = FacilityService()

        df = pd.DataFrame(
            self.service.get_active()
        )

        facility_names = df["name"].tolist()

        self.facility_map = dict(
            zip(
                df["name"],
                df["facility_id"]
            )
        )

        if not facility_names:
            facility_names = ["Keine Sportanlage vorhanden"]

        self.result = None

        self.title(title)
        self.geometry("420x390")
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

        if facility_names:
            self.facility_combo.set(facility_names[0])

        ctk.CTkLabel(
            self,
            text="Trainingszonen",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.training_zones_combo = ctk.CTkComboBox(
            self,
            values=[
                "1",
                "2",
                "4"
            ]
        )

        self.training_zones_combo.pack(
            padx=20,
            fill="x"
        )

        self.training_zones_combo.set("1")    

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

            training_zones = daten.get(
                "training_zones",
                daten.get("TRAININGSZONEN", 1)
            )

            if str(training_zones).lower() == "nan":
                training_zones = 1

            self.training_zones_combo.set(
                str(int(float(training_zones)))
            )

            facility_id = daten.get(
                "facility_id",
                daten.get("FACILITY_ID", "")
            )

            for facility_name, mapped_id in self.facility_map.items():

                if str(mapped_id) == str(facility_id):
                    self.facility_combo.set(
                        facility_name
                    )
                    break

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
            "name": name,
            "facility_id": self.facility_map.get(
                facility_name,
                ""
            ),
            "address": self.address_entry.get().strip(),
            "training_zones": int(
                self.training_zones_combo.get()
            )
        }

        self.destroy()    

    def show(self):

        self.wait_window()

        return self.result    