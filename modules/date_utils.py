"""
=========================================================
ASV Manager
Date Utilities
=========================================================
"""

import pandas as pd


def parse_date(value):
    """
    Akzeptiert:
    - 07.08.2026
    - 2026-08-07
    - echte Excel/Python-Datumswerte
    """

    if pd.isna(value):
        return pd.NaT

    # zuerst österreichisches Format
    datum = pd.to_datetime(
        value,
        format="%d.%m.%Y",
        errors="coerce"
    )

    if not pd.isna(datum):
        return datum

    # danach ISO/Python-Format
    datum = pd.to_datetime(
        value,
        format="%Y-%m-%d",
        errors="coerce"
    )

    if not pd.isna(datum):
        return datum

    # letzte Rettung
    return pd.to_datetime(
        value,
        dayfirst=True,
        errors="coerce"
    )


def format_date(value):
    datum = parse_date(value)

    if pd.isna(datum):
        return ""

    return datum.strftime("%d.%m.%Y")


def format_time(value):
    if pd.isna(value):
        return ""

    text = str(value)

    if len(text) >= 5:
        return text[:5]

    return text


def get_kw(value):
    datum = parse_date(value)

    if pd.isna(datum):
        return None

    return datum.isocalendar().week