from modules.repositories.person_repository import PersonRepository


class PersonService:

    def __init__(self):
        self.repository = PersonRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_person(self, person_id):
        return self.repository.get_by_id(person_id)

    def update_person(
        self,
        person_id,
        first_name,
        last_name,
        birth_date,
        mobile,
        email,
        status,
        active,
        note,
    ):
        self.repository.update(
            person_id,
            first_name,
            last_name,
            birth_date,
            mobile,
            email,
            status,
            active,
            note,
        )
