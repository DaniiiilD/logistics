import pytest
from src.api.handlers.user import UserService
from unittest.mock import AsyncMock

@pytest.fixture
def user_service_mock():
    mock_user_repo = AsyncMock()
    mock_driver_repo = AsyncMock()
    mock_company_repo = AsyncMock()
    mock_redis = AsyncMock()
    
    service = UserService(
        user_repo=mock_user_repo,
        driver_repo=mock_driver_repo,
        company_repo=mock_company_repo,
        redis=mock_redis
    )
    return service