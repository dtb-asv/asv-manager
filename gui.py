"""
=========================================================
ASV Neufeld Manager
GUI Version 2.4 - Zwei-Spalten-Layout
=========================================================
"""
from modules.members_window import MembersWindow
from modules.settings import Settings
from modules.add_game_window import AddGameWindow
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from modules.games_window import GamesWindow
from PIL import Image
from config import *
from version import *
from modules.dashboard import Dashboard
from modules.excel_reader import ExcelReader
from modules.poster_generator import PosterGenerator
from modules.teams_window import TeamsWindow
from modules.configuration_service import ConfigurationService
from modules.roles_window import RolesWindow
from modules.trainings_window import TrainingsWindow
from modules.department_window import DepartmentWindow
from modules.facility_window import FacilityWindow
from modules.place_window import PlaceWindow


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ASVManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(f"{PROGRAMMNAME} {VERSION}")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(1100, 700)
        self.resizable(True, True)

        self.reader = ExcelReader()
        self.poster_generator = PosterGenerator()
        self.settings = Settings()

        self.configuration_service = ConfigurationService()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main()

    def create_sidebar(self):
        sidebar = ctk.CTkScrollableFrame(
            self,
            width=200,
            corner_radius=0
        )
        sidebar.grid(row=0, column=0, sticky="ns")

        logo = CTkImage(
            light_image=Image.open(LOGO),
            dark_image=Image.open(LOGO),
            size=(110, 110)
        )

        ctk.CTkLabel(sidebar, image=logo, text="").pack(pady=(25, 10))

        ctk.CTkLabel(
            sidebar,
            text="ASV Manager",
            font=("Segoe UI", 20, "bold")
        ).pack()

        ctk.CTkLabel(
            sidebar,
            text=f"Version {VERSION}"
        ).pack(pady=(0, 25))

        self.sidebar = sidebar
        
        # -----------------------------
        # Hauptmenü
        # -----------------------------

        self.add_menu_button(
            "🏠 Dashboard"
        )

        # -----------------------------
        # Vereinsverwaltung
        # -----------------------------

        self.add_menu_group("Vereinsverwaltung")

        self.add_menu_button(
            "🏢 Bereiche",
            self.zeige_bereiche
        )
        self.add_menu_button(
            "🏟 Sportanlagen",
            self.zeige_sportanlagen
        )
        self.add_menu_button(
            "⚽ Plätze",
            self.zeige_plaetze
        )

        # -----------------------------
        # Sport
        # -----------------------------

        self.add_menu_group("Sport")

        self.add_menu_button(
            "⚽ Mannschaften",
            self.zeige_mannschaften
        )

        self.add_menu_button(
            "👥 Mitglieder",
            self.zeige_mitglieder
        )

        self.add_menu_button(
            "🏃 Trainings",
            self.zeige_trainings
        )

        self.add_menu_button(
            "📅 Spiele",
            self.zeige_spiele
        )

        self.add_menu_button(
            "➕ Neues Spiel",
            self.neues_spiel
        )

        # -----------------------------
        # Verwaltung
        # -----------------------------

        self.add_menu_group("Verwaltung")

        self.add_menu_button(
            "⚙ Rollen",
            self.zeige_rollen
        )

        self.add_menu_button("🖼 Poster")
        self.add_menu_button("📅 Kalender")
        self.add_menu_button("☁ GitHub")
        self.add_menu_button("⚙ Einstellungen")
        self.add_menu_button("ℹ Info")

    def add_menu_group(self, title):

        font=("Segoe UI", 14, "bold")
        pady=(18, 6)
         

        ctk.CTkLabel(
            self.sidebar,
            text=title,
            font=("Segoe UI", 13, "bold"),
            text_color=("gray40", "gray70")
        ).pack(
            anchor="w",
            padx=18,
            pady=(12, 4)
        )


    def add_menu_button(self, text, command=None):

        ctk.CTkButton(
            self.sidebar,
            text=text,
            width=165,
            command=command
        ).pack(pady=4)        

    def create_main(self):
        main = ctk.CTkFrame(self)
        main.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        main.grid_columnconfigure(0, weight=0)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        control = ctk.CTkFrame(main, width=330)
        control.grid(row=0, column=0, sticky="ns", padx=(0, 15), pady=0)
        control.grid_propagate(False)

        dashboard_area = ctk.CTkFrame(main)
        dashboard_area.grid(row=0, column=1, sticky="nsew", pady=0)

        # -----------------------------
        # Linke Steuerung
        # -----------------------------

        ctk.CTkLabel(
            control,
            text="Steuerung",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))

        ctk.CTkLabel(
            control,
            text="Saison / Excel",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(5, 5))

        self.excel_entry = ctk.CTkEntry(
            control,
            width=285
        )
        self.excel_entry.pack(padx=20, pady=(0, 8))

        ctk.CTkButton(
            control,
            text="📂 Excel auswählen",
            command=self.open_excel
        ).pack(padx=20, pady=(0, 18), fill="x")

        ctk.CTkLabel(
            control,
            text="Kalenderwoche",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 5))

        self.excel_entry.insert(
            0,
            self.settings.get("last_excel")
        )

        self.kw_entry = ctk.CTkEntry(
            control,
            width=90,
            placeholder_text="leer = alle"
        )
        self.kw_entry.pack(anchor="w", padx=20, pady=(0, 18))

        ctk.CTkLabel(
            control,
            text="Aktionen",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 8))

        self.kw_entry.insert(
            0,
            self.settings.get("last_kw")
        )
        
        self.kw_entry.bind(
            "<KeyRelease>",
            lambda event: self.settings.set("last_kw", self.kw_entry.get())
        )

        self.poster = ctk.BooleanVar(value=True)
        self.ics = ctk.BooleanVar(value=True)
        self.github = ctk.BooleanVar(value=True)
        self.zip = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(control, text="Poster erstellen", variable=self.poster).pack(anchor="w", padx=20, pady=5)
        ctk.CTkCheckBox(control, text="ICS erstellen", variable=self.ics).pack(anchor="w", padx=20, pady=5)
        ctk.CTkCheckBox(control, text="GitHub aktualisieren", variable=self.github).pack(anchor="w", padx=20, pady=5)
        ctk.CTkCheckBox(control, text="ZIP erstellen", variable=self.zip).pack(anchor="w", padx=20, pady=5)

        self.progress = ctk.CTkProgressBar(control)
        self.progress.pack(fill="x", padx=20, pady=(30, 10))
        self.progress.set(0)

        ctk.CTkButton(
            control,
            text="START",
            height=45,
            font=("Segoe UI", 18, "bold"),
            command=self.start
        ).pack(padx=20, pady=(10, 15), fill="x")

        ctk.CTkButton(
            control,
            text="🚪 Beenden",
            height=38,
            command=self.destroy
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        self.status = ctk.CTkTextbox(control, height=140)
        self.status.pack(fill="x", padx=20, pady=(0, 20))
        self.status.insert("end", "ASV Manager gestartet...\n")

        # -----------------------------
        # Rechtes Dashboard
        # -----------------------------

        ctk.CTkLabel(
            dashboard_area,
            text="Dashboard",
            font=("Segoe UI", 28, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.dashboard = Dashboard(dashboard_area)

    def open_excel(self):
        file = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx")]
        )

        if file:
            self.excel_entry.delete(0, "end")
            self.excel_entry.insert(0, file)
            self.settings.set(
               "last_excel",
                file
            )

            self.reader.load(file)

            self.configuration_service.ensure_configuration_sheets(file)

            stats = self.reader.statistik()
            spiel = self.reader.naechstes_spiel()

            self.dashboard.update_stats(stats)
            self.dashboard.update_next_game(spiel)

            self.status.insert(
                "end",
                f"Excel geladen:\n{file}\n"
            )
    def neues_spiel(self):

        excel_datei = self.excel_entry.get().strip()

        if not excel_datei:
            messagebox.showwarning(
                "Excel fehlt",
                "Bitte zuerst eine Excel-Datei auswählen."
            )
            return

        AddGameWindow(
            self,
            excel_datei,
            on_saved=self.reload_excel
        )
    def reload_excel(self):

        excel_datei = self.excel_entry.get()

        if excel_datei:
            self.reader.load(excel_datei)

            stats = self.reader.statistik()
            spiel = self.reader.naechstes_spiel()

            self.dashboard.update_stats(stats)
            self.dashboard.update_next_game(spiel)

            self.status.insert(
                "end",
                "Excel wurde nach neuem Spiel aktualisiert.\n"
            ) 

    def zeige_spiele(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showerror(
                "Fehler",
                "Bitte zuerst eine Excel-Datei auswählen."
            )
            return

        GamesWindow(self, excel_datei)   

    def zeige_trainings(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        TrainingsWindow(self, excel_datei)      

    def zeige_bereiche(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        DepartmentWindow(self, excel_datei)    

    def zeige_sportanlagen(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        FacilityWindow(
            self,
            excel_datei
        )   

    def zeige_plaetze(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        PlaceWindow(
            self,
            excel_datei
        )               

    def start(self):
        self.status.insert(
            "end",
            "\nStarte Verarbeitung...\n"
        )

        excel_datei = self.excel_entry.get()
        kw = self.kw_entry.get()
        self.settings.set(
            "last_kw",
            kw
        )

        if self.poster.get():
            self.status.insert(
                "end",
                "▶ Poster Generator gestartet\n"
            )

            self.poster_generator.create(
                excel_datei,
                kw
            )

            self.status.insert(
                "end",
                "✔ Poster Generator beendet\n"
            )

        self.progress.set(1)


    def zeige_mitglieder(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen."
            )
            return

        MembersWindow(self, excel_datei)

    def zeige_mannschaften(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        TeamsWindow(self, excel_datei)    

    def zeige_rollen(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        RolesWindow(self, excel_datei)    

def start_gui():
    app = ASVManager()
    app.mainloop()   