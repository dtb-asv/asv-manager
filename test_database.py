from modules.database import Database


def main():
    db = Database()

    try:
        connection = db.connect()

        cursor = connection.cursor()
        cursor.execute("SELECT current_database(), version();")

        database_name, version = cursor.fetchone()

        print("===================================")
        print("Verbindung erfolgreich")
        print("===================================")
        print(f"Datenbank : {database_name}")
        print(f"Version   : {version}")

        cursor.close()

    except Exception as e:
        print("===================================")
        print("VERBINDUNG FEHLGESCHLAGEN")
        print("===================================")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    main()