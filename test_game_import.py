from modules.services.game_import_service import GameImportService


service = GameImportService()

service.import_excel(
    r"C:\Users\DTB\asv-manager\Excel\Terminefussball_2026_Herbst.xlsx"
)
