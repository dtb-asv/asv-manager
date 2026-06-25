"""
=========================================================
ASV Manager
Date Utilities
=========================================================
Alle Datums- und Zeitfunktionen befinden sich hier.
"""

import pandas as pd


def parse_date(value):
    """
    Wandelt ein Datum aus Excel in ein Python-Datum um.
    Erwartetes Format:
    TT.MM.JJJJ
    """

    return pd.to_datetime(
        value,
        format="%d.%m.%Y",
        errors="coerce"
    )


def format_date(value):
    """
    Gibt ein Datum im Format TT.MM.JJJJ zurück.
    """

    datum = parse_date(value)

    if pd.isna(datum):
        return ""

    return datum.strftime("%d.%m.%Y")


def format_time(value):
    """
    Uhrzeit schön darstellen.
    """

    if pd.isna(value):
        return ""

    text = str(value)

    if len(text) >= 5:
        return text[:5]

    return text


def get_kw(value):
    """
    Kalenderwoche berechnen.
    """

    datum = parse_date(value)

    if pd.isna(datum):
        return None

    return datum.isocalendar().week