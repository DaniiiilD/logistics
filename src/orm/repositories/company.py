from src.orm.models.company import Company
from src.orm.repositories.base import BaseRepository


class CompanyRepository(BaseRepository):
    model = Company
