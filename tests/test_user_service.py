import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock
from src.api.handlers.user import UserService
from src.schemas.responses.users import DriverProfileResponse, CompanyProfileResponse
from src.schemas.requests.users import DriverUpdate, CompanyUpdate
from src.core.constants import Role
from src.core.security import hash_tg_id
from unittest.mock import patch, ANY

async def test_get_user_by_email_success(user_service_mock):

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

async def test_update_driver_profile_no_data(user_service_mock):
    """ тест на ошибку 400: нет данных для обновления"""
    empty_data = DriverUpdate()
    
    with pytest.raises(HTTPException) as excinfo:
        await user_service_mock.update_driver_profile(user_id = 1, data= empty_data)
        
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Нет данных для обновления"
    
async def test_update_driver_profile_user_not_found(user_service_mock):
    """ тест ошибки 404, если у пользователь не найден в бд при обновлении"""
    updated_data = DriverUpdate(full_name="Новое Имя")
    
    user_service_mock.user_repo.get_by_id.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        await user_service_mock.update_driver_profile(user_id=999, data=updated_data)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Пользователь не найден"
    
async def test_update_driver_profile_success(user_service_mock):
    """ успешный сценарий обновления email и профиля водителя"""
    updated_data = DriverUpdate(email ='new@test.com', full_name ='Иван Новый')
    
    mock_user = MagicMock(id=1, email="old@test.com")
    mock_driver = MagicMock(id=5, full_name="Старое Имя")
    
    user_service_mock.user_repo.get_by_id.return_value = mock_user
    user_service_mock.driver_repo.get_by_user_id.return_value = mock_driver
    
    mock_updated_user = MagicMock(
        id=1,
        email="new@test.com",
        role='driver',
        driver=MagicMock(full_name="Иван Новый", phone='123', transport_type='Грузовик')
    )
    user_service_mock.user_repo.get_with_driver.return_value = mock_updated_user
    
    result = await user_service_mock.update_driver_profile(user_id=1, data=updated_data)
    
    assert isinstance(result, DriverProfileResponse)
    assert result.full_name == "Иван Новый"
    assert result.email == "new@test.com"
    
    user_service_mock.user_repo.update.assert_called_once_with(1, {"email": "new@test.com"})
    user_service_mock.driver_repo.update.assert_called_once_with(5, {"full_name": "Иван Новый"})

async def test_link_telegram_account_success(user_service_mock):
    """Успешная привязка тг аккаунта"""
    user_service_mock.redis.get.return_value = '10'
    
    await user_service_mock.link_telegram_account(token="valid_token", telegram_id=123456789)
    
    user_service_mock.redis.delete.assert_called_once_with('tg_link:valid_token')
    
    user_service_mock.user_repo.update.assert_called_once()
    
    called_args, _ = user_service_mock.user_repo.update.call_args
    assert called_args[0] == 10
    assert "telegram_hash_id" in called_args[1]
    assert "telegram_id_encrypted" in called_args[1]
    
async def test_vetify_login_user_wrong_code(user_service_mock):
    """Возвращает False, если введенный код не совпалает с кодом в редис"""
    user_service_mock.redis.get.return_value = "111111"
    
    result = await user_service_mock.verify_login_user(
        email='test@test.com', code="222222", telegram_id=123
    )

    assert result is False
    user_service_mock.user_repo.update.assert_not_called()
    
async def test_vetify_login_user_success(user_service_mock):
    """ Успешная верификация кода и обновления Telegram данных в БД"""
    user_service_mock.redis.get.return_value = "123456"
    
    mock_user = MagicMock(id=42, email='test@test.com')
    user_service_mock.user_repo.get_user_by_email.return_value = mock_user
    
    result = await user_service_mock.verify_login_user(
        email="test@test.com", code ='123456', telegram_id=123456789
    )
    
    assert result is True
    
    user_service_mock.user_repo.update.assert_called_once()
    called_args, _ = user_service_mock.user_repo.update.call_args
    assert called_args[0] == 42
    assert "telegram_hash_id" in called_args[1]
    assert "telegram_id_encrypted" in called_args[1]
    
async def test_company_profile_success(user_service_mock):
    """ Успешное получение профиля компании с правильными полями"""
    mock_company = MagicMock(
        company_name ="ООО перевозки",
        rep_full_name ="Сашка Саша",
        phone="555-555",
        ttn="12345678",
    )
    mock_user = MagicMock(
            id=2,
            email="company@test.com",
            role=Role.COMPANY,
            company=mock_company
        )
    user_service_mock.user_repo.get_with_company.return_value = mock_user
        
    result = await user_service_mock.get_company_profile(user_id=2)
    
    assert isinstance(result, CompanyProfileResponse)
    assert result.company_name == "ООО перевозки"
    assert result.rep_full_name == "Сашка Саша"
    assert result.id == 2
    
async def test_update_company_profile_success(user_service_mock):
    """успешное обновление email и данных компании в БД"""
    updated_data = CompanyUpdate(email="new_company@test.com", company_name = "ООО Новые Перевозки")
    
    mock_user = MagicMock(email="old_company@gmail.com")
    mock_user.id = 2
    
    mock_company = MagicMock(user_id = 2, company_name = "ООО Старые Перевозки")
    mock_company.id = 10
    
    user_service_mock.user_repo.get_by_id.return_value = mock_user
    user_service_mock.company_repo.get_by_user_id.return_value = mock_company

    mock_updated_user = MagicMock(
        email="new_company@test.com",
        role=Role.COMPANY,
        company = MagicMock(
            company_name="ООО Новые Перевозки",
            rep_full_name = "Сергей Петров",
            phone = "555 555",
            ttn ="12345678",
        )
    )
    mock_updated_user.id = 2
    
    user_service_mock.user_repo.get_with_company.return_value = mock_updated_user
    
    result = await user_service_mock.update_company_profile(user_id=2, data=updated_data)
    
    assert isinstance(result, CompanyProfileResponse)
    assert result.company_name == "ООО Новые Перевозки"
    assert result.email == "new_company@test.com"
    
    user_service_mock.user_repo.update.assert_called_once_with(2, {"email": "new_company@test.com"})
    user_service_mock.company_repo.update.assert_called_once_with(10, {"company_name": "ООО Новые Перевозки"})
    
async def test_update_company_profile_no_data(user_service_mock):
    """ тест на 404, нет данных для обновления компании"""
    empty_data = CompanyUpdate()
    with pytest.raises(HTTPException) as excinfo:
        await user_service_mock.update_company_profile(user_id=2, data=empty_data)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Нет данных для обновления"
    
async def test_update_company_profile_user_not_found(user_service_mock):
    """ тест на 404, если компания не найдена в БД при обновлении"""
    updated_data = CompanyUpdate(company_name="Новая Компания")
    user_service_mock.user_repo.get_by_id.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        await user_service_mock.update_company_profile(user_id=999, data=updated_data)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Пользователь не найден"
    
async def test_create_telegram_link_token_success(user_service_mock):
    """ Успешная генериция токена привязки и запись в redis"""
    user_id = 42
    
    token = await user_service_mock.create_telegram_link_token(user_id)
    
    assert isinstance(token, str)
    assert len(token) == 36
    
    user_service_mock.redis.setex.assert_called_once_with(f"tg_link:{token}", 600, user_id)
    
async def test_get_user_by_tg_id_success(user_service_mock):
    """ Получение пользователя по tg id"""
    
    tg_id = 123456789
    expected_hash = hash_tg_id(tg_id)
    user_service_mock.user_repo.get_user_by_tg_hash.return_value = "mocked_user_object"
    
    result = await user_service_mock.get_user_by_tg_id(tg_id=tg_id)
    
    assert result == 'mocked_user_object'
    user_service_mock.user_repo.get_user_by_tg_hash.assert_called_once_with(expected_hash)
    
    
@patch("src.api.handlers.user.send_notification_email")
async def test_send_login_code_success(mock_send_email, user_service_mock):
    """ Генерация кода, запись в редис и вызов celery"""
    test_email = "driver@test.com"
    
    result = await user_service_mock.send_login_code(email=test_email)
    
    assert result is True
    
    user_service_mock.redis.setex.assert_called_once_with(
        f"auth_code:{test_email}", 300, ANY
    )
    
    mock_send_email.delay.assert_called_once()
    
    called_args, called_kwargs = mock_send_email.delay.call_args
    assert called_kwargs.get("email") == test_email
    assert called_kwargs.get("order_id") == 0
    assert "Ваш код для входа в Telegram-бот" in called_kwargs.get("message")