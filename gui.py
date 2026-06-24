"""
=========================================================
ASV Neufeld Manager
GUI Version 2.0.2
=========================================================
"""

import customtkinter as ctk
from modules.dashboard import Dashboard
from modules.excel_reader import ExcelReader
from customtkinter import CTkImage
from tkinter import filedialog
from PIL import Image

from config import *
from version import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ASVManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(f"{PROGRAMMNAME} {VERSION}")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)

        # ==========================
        # Hauptlayout
        # ==========================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main()
        self.reader = ExcelReader()

    # -------------------------------------------------

    def create_sidebar(self):

        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="ns")

        logo = CTkImage(
            light_image=Image.open(LOGO),
            dark_image=Image.open(LOGO),
            size=(120,120)
        )

        ctk.CTkLabel(
            sidebar,
            image=logo,
            text=""
        ).pack(pady=(30,10))

        ctk.CTkLabel(
            sidebar,
            text="ASV Manager",
            font=("Segoe UI",22,"bold")
        ).pack()

        ctk.CTkLabel(
            sidebar,
            text=f"Version {VERSION}"
        ).pack(pady=(0,25))

        menues = [
            "🏠 Dashboard",
            "🖼 Poster",
            "📅 Kalender",
            "☁ GitHub",
            "⚙ Einstellungen",
            "ℹ Info"
        ]

        for m in menues:

            ctk.CTkButton(
                sidebar,
                text=m,
                width=180
            ).pack(pady=6)

    # -------------------------------------------------

    def create_main(self):

        main = ctk.CTkFrame(self)
        main.grid(row=0,column=1,sticky="nsew",padx=20,pady=20)

        title = ctk.CTkLabel(
            main,
            text="Dashboard",
            font=("Segoe UI",28,"bold")
        )

        title.pack(anchor="w", pady=(10,25))
        self.dashboard = Dashboard(main)

        # ----------------------
        # Excel
        # ----------------------

        excel_frame = ctk.CTkFrame(main)

        excel_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            excel_frame,
            text="Saison"
        ).pack(anchor="w", padx=15,pady=(10,0))

        self.excel_entry = ctk.CTkEntry(
            excel_frame,
            width=550
        )

        self.excel_entry.pack(side="left", padx=15,pady=15)

        ctk.CTkButton(
            excel_frame,
            text="Öffnen",
            command=self.open_excel
        ).pack(side="left")

        # ----------------------
        # Kalenderwoche
        # ----------------------

        kw_frame = ctk.CTkFrame(main)

        kw_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            kw_frame,
            text="Kalenderwoche (leer = alle)"
        ).pack(anchor="w", padx=15,pady=(10,0))

        self.kw_entry = ctk.CTkEntry(
            kw_frame,
            width=80
        )

        self.kw_entry.pack(anchor="w", padx=15,pady=15)

        # ----------------------
        # Aktionen
        # ----------------------

        action = ctk.CTkFrame(main)

        action.pack(fill="x", pady=10)

        self.poster = ctk.BooleanVar(value=True)
        self.ics = ctk.BooleanVar(value=True)
        self.github = ctk.BooleanVar(value=True)
        self.zip = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(action,text="Poster",variable=self.poster).pack(anchor="w",padx=15,pady=5)
        ctk.CTkCheckBox(action,text="ICS",variable=self.ics).pack(anchor="w",padx=15,pady=5)
        ctk.CTkCheckBox(action,text="GitHub",variable=self.github).pack(anchor="w",padx=15,pady=5)
        ctk.CTkCheckBox(action,text="ZIP",variable=self.zip).pack(anchor="w",padx=15,pady=5)

        # ----------------------
        # Progress
        # ----------------------

        self.progress = ctk.CTkProgressBar(main)

        self.progress.pack(fill="x", pady=25)

        self.progress.set(0)

        self.status = ctk.CTkTextbox(main,height=120)

        self.status.pack(fill="x")

        self.status.insert("end","ASV Manager gestartet...\n")

        ctk.CTkButton(
            main,
            text="START",
            height=45,
            font=("Segoe UI",18,"bold"),
            command=self.start
        ).pack(pady=25)

    # -------------------------------------------------

    def open_excel(self):

        file = filedialog.askopenfilename(
            filetypes=[("Excel","*.xlsx")]
        )

        if file:

           self.excel_entry.delete(0, "end")
           self.excel_entry.insert(0, file)

           self.reader.load(file)

           stats = self.reader.statistik()

           spiel = self.reader.naechstes_spiel()

           self.dashboard.update_next_game(spiel)

           self.dashboard.update_stats(stats)

           self.status.insert(
            "end",
           f"Excel geladen:\n{file}\n"
        )

    # -------------------------------------------------

    def start(self):

        self.progress.set(0.2)
        self.status.insert("end","\nStarte Verarbeitung...\n")

        if self.poster.get():
            self.status.insert("end","✔ Poster aktiviert\n")

        if self.ics.get():
            self.status.insert("end","✔ ICS aktiviert\n")

        if self.github.get():
            self.status.insert("end","✔ GitHub aktiviert\n")

        if self.zip.get():
            self.status.insert("end","✔ ZIP aktiviert\n")

        self.progress.set(1)


def start_gui():

    app = ASVManager()

    app.mainloop()