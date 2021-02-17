from src.repositories.repository import WebsiteRepository

repo = WebsiteRepository()

print(repo.get_by_id(15))