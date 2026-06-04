import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock
from src.api.handlers.user import UserService
from src.schemas.responses.users import DriverProfileResponse

async def test_verify_code(user_service_mock):

    repo = user_service_mock.user_repo
    repo.get_user_by_email.return_value = "fake_user"
    
    result = await user_service_mock.get_user_by_email("test@test.com")

    assert result == "fake_user"
    
async def test_driver_profile_success(user_service_mock):
    
    mock_driver = MagicMock(full_name="Иван", phone="123", transport_type ="Грузовик")
    mock_user = MagicMock(id=1, email="test@test.com", role="driver", driver=mock_driver)
    
    user_service_mock.user_repo.get_with_driver.return_value = mock_user
    
    result = await user_service_mock.get_driver_profile(user_id=1)
    
    assert isinstance(result, DriverProfileResponse)
    assert result.full_name == "Иван"
    assert result.phone == "123"
    
async def test_driver_profile_not_found(user_service_mock):
    
    user_service_mock.user_repo.get_with_driver.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        await user_service_mock.get_driver_profile(user_id=999)
        
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Профиль водителя не найден"
