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
from datetime import date, timedelta
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
from modules.training_plan_window import TrainingPlanWindow
from modules.dashboard_service import DashboardService


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
        self.system_status = "green"
        self.dashboard_service = DashboardService()

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
            "📆 Trainingsplan",
            self.zeige_trainingsplan
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

        # =====================================================
        # Hauptarbeitsbereich
        # =====================================================

        main = ctk.CTkFrame(self)
        main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=15,
            pady=15
        )

        main.grid_columnconfigure(0, weight=0)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # =====================================================
        # Linker Werkzeugbereich
        # =====================================================

        control = ctk.CTkScrollableFrame(
            main,
            width=330
        )
        control.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 15)
        )

        ctk.CTkLabel(
            control,
            text="Werkzeuge",
            font=("Segoe UI", 24, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        ctk.CTkLabel(
            control,
            text="Saison / Excel",
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )

        self.excel_entry = ctk.CTkEntry(
            control,
            width=285
        )
        self.excel_entry.pack(
            padx=20,
            pady=(0, 8),
            fill="x"
        )

        self.excel_entry.insert(
            0,
            self.settings.get("last_excel")
        )

        ctk.CTkButton(
            control,
            text="📂 Excel auswählen",
            command=self.open_excel
        ).pack(
            padx=20,
            pady=(0, 18),
            fill="x"
        )

        ctk.CTkLabel(
            control,
            text="Kalenderwoche",
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )

        self.kw_entry = ctk.CTkEntry(
            control,
            width=90,
            placeholder_text="leer = alle"
        )
        self.kw_entry.pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        self.kw_entry.insert(
            0,
            self.settings.get("last_kw")
        )

        self.kw_entry.bind(
            "<KeyRelease>",
            lambda event: self.settings.set(
                "last_kw",
                self.kw_entry.get()
            )
        )

        ctk.CTkLabel(
            control,
            text="Aktionen",
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        self.poster = ctk.BooleanVar(value=True)
        self.ics = ctk.BooleanVar(value=True)
        self.github = ctk.BooleanVar(value=True)
        self.zip = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            control,
            text="Poster erstellen",
            variable=self.poster
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        ctk.CTkCheckBox(
            control,
            text="ICS erstellen",
            variable=self.ics
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        ctk.CTkCheckBox(
            control,
            text="GitHub aktualisieren",
            variable=self.github
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        ctk.CTkCheckBox(
            control,
            text="ZIP erstellen",
            variable=self.zip
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        self.progress = ctk.CTkProgressBar(control)
        self.progress.pack(
            fill="x",
            padx=20,
            pady=(30, 10)
        )
        self.progress.set(0)

        ctk.CTkButton(
            control,
            text="START",
            height=45,
            font=("Segoe UI", 18, "bold"),
            command=self.start
        ).pack(
            padx=20,
            pady=(10, 15),
            fill="x"
        )

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

        self.status = ctk.CTkTextbox(
            control,
            height=140
        )
        self.status.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.status.insert(
            "end",
            "ASV Manager gestartet...\n"
        )

        # =====================================================
        # Rechte Vereinszentrale
        # =====================================================

        dashboard_area = ctk.CTkScrollableFrame(main)
        dashboard_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # =====================================================
        # Aktuelle Kalenderwoche
        # =====================================================

        heute = date.today()
        montag = heute - timedelta(days=heute.weekday())
        sonntag = montag + timedelta(days=6)
        kalenderwoche = heute.isocalendar().week

        # =====================================================
        # Kopfbereich
        # =====================================================

        header = ctk.CTkFrame(
            dashboard_area,
            corner_radius=12
        )
        header.pack(
            fill="x",
            padx=5,
            pady=(5, 15)
        )

        ctk.CTkLabel(
            header,
            text="Vereinszentrale",
            font=("Segoe UI", 30, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 3)
        )

        ctk.CTkLabel(
            header,
            text=(
                f"KW {kalenderwoche}  |  "
                f"{montag.strftime('%d.%m.%Y')} – "
                f"{sonntag.strftime('%d.%m.%Y')}"
            ),
            font=("Segoe UI", 15),
            text_color=("gray35", "gray75")
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        self.system_status_label = ctk.CTkLabel(
            header,
            text="🟢 System bereit",
            font=("Segoe UI", 15, "bold"),
            corner_radius=8,
            padx=12,
            pady=7,
            fg_color="#1E7D34"
        )

        self.system_status_label.place(
            relx=0.97,
            rely=0.5,
            anchor="e"
        )

        # =====================================================
        # Übersichtskarten
        # =====================================================

        cards_frame = ctk.CTkFrame(
            dashboard_area,
            fg_color="transparent"
        )
        cards_frame.pack(
            fill="x",
            padx=5,
            pady=(0, 15)
        )

        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        def create_card(
            parent,
            row,
            column,
            title,
            value,
            detail,
            button_text=None,
            command=None
        ):

            card = ctk.CTkFrame(
                parent,
                corner_radius=12,
                border_width=1,
                border_color=("gray75", "gray30")
            )

            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=7,
                pady=7
            )

            # Schmale Akzentleiste oben
            ctk.CTkFrame(
                card,
                height=5,
                corner_radius=3,
                fg_color=("gray25", "gray75")
            ).pack(
                fill="x",
                padx=12,
                pady=(12, 2)
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 19, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(10, 8)
            )

            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Segoe UI", 27, "bold")
            )
            value_label.pack(
                anchor="w",
                padx=20,
                pady=(0, 2)
            )

            detail_label = ctk.CTkLabel(
                card,
                text=detail,
                font=("Segoe UI", 13),
                justify="left",
                anchor="w",
                text_color=("gray35", "gray70")
            )

            detail_label.pack(
                anchor="w",
                fill="x",
                padx=20,
                pady=(0, 15)
            )

            if command:

                card.bind("<Button-1>", lambda e: command())

                for widget in card.winfo_children():
                    widget.bind("<Button-1>", lambda e: command())

            if button_text:

                ctk.CTkButton(
                    card,
                    text=button_text,
                    height=32,
                    command=command
                ).pack(
                    anchor="w",
                    padx=20,
                    pady=(0, 18)
                )

            card.value_label = value_label
            card.detail_label = detail_label    

            return card

        self.week_card = create_card(
            cards_frame,
            0,
            0,
            "🗓 Diese Woche",
            "Noch keine Saison geladen",
            "Trainings, Spiele und Termine",
            "Saison auswählen",
            self.open_excel
        )

        self.training_card = create_card(
            cards_frame,
            0,
            1,
            "🏃 Training",
            "–",
            "Trainingsplan und konkrete Einheiten",
            "Trainingsplan öffnen",
            self.zeige_trainingsplan
        )

        self.games_card = create_card(
            cards_frame,
            1,
            0,
            "⚽ Spiele",
            "–",
            "Meisterschaft, Freundschaftsspiele und Turniere",
            "Spiele öffnen",
            self.zeige_spiele
        )

        self.finance_card = create_card(
            cards_frame,
            1,
            1,
            "💰 Finanzen",
            "Modul folgt",
            "Beiträge, Rechnungen und Sponsoren"
        )

        # =====================================================
        # Bestehendes Dashboard
        # =====================================================

        dashboard_container = ctk.CTkFrame(
            dashboard_area,
            corner_radius=12
        )
        dashboard_container.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            dashboard_container,
            text="Saisonübersicht",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.dashboard = Dashboard(
            dashboard_container
        )

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

            dashboard_stats = {
                "Spiele diese Woche": stats.get("Diese Woche", 0),
                "Trainings diese Woche": "-",
                "Trainings heute": "-",
                "Nächstes Spiel": 1 if self.reader.naechstes_spiel() else 0,
                "Nächstes Training": "-",
                "Offene Aufgaben": "-",
                "Konflikte": "-"
            }

            self.dashboard.update_stats(dashboard_stats)

            spiel = self.reader.naechstes_spiel()
            self.dashboard.update_next_game(spiel)
            self.update_dashboard_cards()

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
            self.update_dashboard_cards()

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

    def zeige_trainingsplan(self):

        excel_datei = self.excel_entry.get()

        if not excel_datei:
            messagebox.showwarning(
                "Saison fehlt",
                "Bitte zuerst eine Saison öffnen.",
                parent=self
            )
            return

        TrainingPlanWindow(
            self,
            excel_datei
        )   

    def zeige_bereiche(self):
        DepartmentWindow(self)  

    def zeige_sportanlagen(self):

        FacilityWindow(self)
         
    def zeige_plaetze(self):

        PlaceWindow(self)

    def update_dashboard_cards(self):
        """
        Aktualisiert die vier Karten der Vereinszentrale.
        """

        try:
            stats = self.reader.statistik()
            training = self.reader.trainings_statistik()
            next_training = self.reader.naechstes_training()
            next_game = self.reader.naechstes_spiel()

            # Karte: Diese Woche
            spiele = stats.get("Diese Woche", 0)
            trainings = training.get("woche", 0)

            self.week_card.value_label.configure(
                text=f"{spiele} Spiele"
            )

            self.week_card.detail_label.configure(
                text=(
                    f"{trainings} Trainings\n"
                    f"KW {date.today().isocalendar().week}"
                )
            )

            # Karte: Training
            if next_training:

                team = next_training.get("TEAM", "-")
                datum = next_training.get("DATUM", "")
                zeit = next_training.get("STARTZEIT", "")
                ort = next_training.get("ORT", "-")

                self.training_card.value_label.configure(
                    text=f"{team}\n{datum}\n{zeit}\n{ort}"
                )
                self.training_card.detail_label.configure(
                    text=(
                        f"Heute: {training['heute']}\n"
                        f"Diese Woche: {training['woche']}\n"
                        f"Aktive Pläne: {training['aktive_plaene']}"
                    )
                )

            else:

                self.training_card.value_label.configure(
                    text="Kein Training geplant"
                )

            # Karte: Spiele
            if next_game:

                liga = (
                    next_game.get("liga")
                    or next_game.get("LIGA")
                    or "-"
                )

                gegner = (
                    next_game.get("gegner")
                    or next_game.get("GEGNER")
                    or "-"
                )

                datum = (
                    next_game.get("datum")
                    or next_game.get("DATUM")
                    or ""
                )

                start = (
                    next_game.get("startzeit")
                    or next_game.get("STARTZEIT")
                    or ""
                )

                ort = (
                    next_game.get("ort")
                    or next_game.get("ORT")
                    or ""
                )

                self.games_card.value_label.configure(
                    text=(
                        f"{liga}\n"
                        f"{gegner}\n"
                        f"{datum}  {start}\n"
                        f"{ort}"
                    )
                )
                self.games_card.detail_label.configure(
                    text=f"{datum}  {start}\n{ort}"
                )
            else:
                self.games_card.detail_label.configure(
                    text="Zurzeit ist kein Spiel geplant."
                )

            # Karte: Finanzen
            self.finance_card.value_label.configure(
                text="In Vorbereitung"
            )

            self.finance_card.detail_label.configure(
                text=(
                    "Mitgliedsbeiträge\n"
                    "Sponsoren\n"
                    "Rechnungen"
                )
            )

        except Exception as e:
            print("Dashboard:", e)                  

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

        MembersWindow(self)

    def zeige_mannschaften(self):
        TeamsWindow(self) 

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

    def update_system_status(self, level, text):

        colors = {
            "green": ("#1E7D34", "#1E7D34"),
            "yellow": ("#C78A00", "#C78A00"),
            "red": ("#B22222", "#B22222"),
        }

        icons = {
            "green": "🟢",
            "yellow": "🟡",
            "red": "🔴",
        }

        self.system_status_label.configure(
            text=f"{icons[level]} {text}",
            fg_color=colors[level]
        )     

def start_gui():
    app = ASVManager()
    app.mainloop()   