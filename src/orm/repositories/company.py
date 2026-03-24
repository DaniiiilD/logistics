from sqlalchemy.ext.asyncio import AsyncSession
from src.orm.models.company import Company
from src.orm.repositories.base import BaseRepository

class CompanyRepository(BaseRepository):
    model = Company

    async def create(self, user_id: int, company_name: str, ttn: str,
               phone: str, rep_full_name: str) -> Company:
        company = Company(
            user_id=user_id,
            company_name=company_name,
            ttn=ttn,
            phone=phone,
            rep_full_name=rep_full_name
        )
        self.session.add(company)
        return company