from modules.repositories.department_repository import DepartmentRepository


class DepartmentService:

    def __init__(self):
        self.repository = DepartmentRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_active(self):
        return self.repository.get_active()

    def get_by_id(self, department_id):
        return self.repository.get_by_id(department_id)

    def save_department(self, daten):

        department = {
            "department_id": daten.get(
                "department_id",
                daten.get("DEPARTMENT_ID")
            ),
            "name": daten.get(
                "name",
                daten.get("NAME", "")
            ),
            "active": daten.get(
                "active",
                daten.get("AKTIV", True)
            ),
        }

        if isinstance(department["active"], str):
            department["active"] = (
                department["active"].strip().lower()
                in ("ja", "true", "1", "aktiv")
            )

        return self.repository.save(department)

    def archive_department(self, department_id):
        self.repository.archive(department_id)