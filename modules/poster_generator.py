"""
=========================================================
ASV Manager
Poster Generator
=========================================================
Erstellt Wochenposter aus der Excel-Datei.
"""

import os
from datetime import datetime, timedelta

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


class PosterGenerator:

    def __init__(self):
        self.background_path = "Hintergrund/background.jpg"
        self.output_folder = "Output"

        self.image_width = 1080
        self.image_height = 1350

        self.y_start = 220
        self.block_height = 130
        self.max_spiele = 7

    def create(self, excel_datei, kw=None):
        """
        Erstellt Poster.
        kw leer = alle Wochen
        kw Zahl = nur diese Kalenderwoche
        """

        if not excel_datei:
            print("Keine Excel-Datei ausgewählt.")
            return False

        df = pd.read_excel(excel_datei, sheet_name="ICS2")
        df["DATUM"] = pd.to_datetime(df["DATUM"], errors="coerce")
        df = df.dropna(subset=["DATUM"])

        # Nur Nachwuchs: KM und U23 ausschließen
        df = df[~df["LIGA"].astype(str).str.contains("KM|U23", case=False, na=False)]

        df["KW"] = df["DATUM"].dt.isocalendar().week
        jahr = int(df["DATUM"].dt.year.mode()[0])

        if kw:
            wochen = [int(kw)]
        else:
            wochen = sorted(df["KW"].dropna().unique())

        font_title = ImageFont.truetype("arial.ttf", 60)
        font_big = ImageFont.truetype("arial.ttf", 45)
        font_small = ImageFont.truetype("arial.ttf", 28)
        font_kw = ImageFont.truetype("arial.ttf", 38)

        for aktuelle_kw in wochen:
            df_woche = df[df["KW"] == aktuelle_kw].sort_values(by="DATUM")

            if df_woche.empty:
                continue

            folder = os.path.join(
                self.output_folder,
                str(jahr),
                f"KW{aktuelle_kw}"
            )
            os.makedirs(folder, exist_ok=True)

            count = 0
            seite = 1

            img = self.neues_bild()
            draw = ImageDraw.Draw(img)

            self.header(draw, aktuelle_kw)

            y = self.y_start

            for _, row in df_woche.iterrows():

                if count == self.max_spiele:
                    img.convert("RGB").save(
                        os.path.join(folder, f"Spielplan_KW{aktuelle_kw}_Seite_{seite}.png")
                    )

                    seite += 1
                    count = 0

                    img = self.neues_bild()
                    draw = ImageDraw.Draw(img)

                    self.header(draw, aktuelle_kw)
                    y = self.y_start

                liga = str(row.get("LIGA", ""))
                gegner = str(row.get("GEGNER", ""))
                datum = row["DATUM"].strftime("%d.%m.%Y")
                zeit = str(row.get("STARTZEIT", ""))
                ort = str(row.get("ORT", ""))
                typ = str(row.get("TYP", "")).strip().lower()

                if typ == "heim":
                    label = "Heim"
                    spiel = f"ASV Neufeld vs {gegner}"
                else:
                    label = "Auswärts"
                    spiel = f"{gegner} vs ASV Neufeld"

                draw.text((50, y), liga, font=font_big, fill="white")

                text = f"{datum} | {zeit} Uhr | {label} {ort}"
                draw.text((220, y + 10), text, font=font_small, fill=(220, 220, 220))

                draw.text((220, y + 55), spiel.upper(), font=font_small, fill="white")

                draw.line((50, y + 110, 1000, y + 110), fill=(255, 255, 255, 60), width=1)

                y += self.block_height
                count += 1

            img.convert("RGB").save(
                os.path.join(folder, f"Spielplan_KW{aktuelle_kw}_Seite_{seite}.png")
            )

        print("Poster erfolgreich erstellt.")
        return True

    def neues_bild(self):
        img = Image.open(self.background_path).convert("RGBA")
        img = img.resize((self.image_width, self.image_height))

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 120))

        return Image.alpha_composite(img, overlay)

    def header(self, draw, kw):
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_kw = ImageFont.truetype("arial.ttf", 38)

        draw.text((50, 50), "SPIELPLAN NACHWUCHS", font=font_title, fill="white")
        draw.text((50, 120), f"KW {kw}", font=font_kw, fill=(200, 200, 200))