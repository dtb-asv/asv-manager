"""
Datenbank-Konfiguration

Lokal:
- verwendet die bisherigen PostgreSQL-Zugangsdaten

Online:
- verwendet automatisch DATABASE_URL, zum Beispiel auf Railway
"""

import os


DATABASE_URL = os.getenv("DATABASE_URL")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "asv_manager"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "Hochzeit2012!!"),
}