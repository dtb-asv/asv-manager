from modules.repositories.member_repository import MemberRepository

repo = MemberRepository()

print("===================================")
print("PERSONEN IN DER DATENBANK")
print("===================================")

print(repo.count())