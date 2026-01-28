"""Фикстуры для UNIT-тестов."""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from app.schemas import UserRole, UserSchema


@pytest.fixture
def mock_async_session():
    """Мок асинхронной сессии БД для unit-тестов."""
    session = AsyncMock()

    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.scalar = AsyncMock()

    # Для работы с контекстным менеджером
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)

    return session


@pytest.fixture
def mock_login_data():
    """Данные для входа пользователя."""
    from app.schemas import UserLogin

    return UserLogin(email='test@example.com', password='password123')


@pytest.fixture
def mock_token_repo(mock_async_session):
    """Мок репозитория токенов."""
    from app.repositories import TokenRepository

    repo = MagicMock(spec=TokenRepository)
    repo.session = mock_async_session

    repo.get_by_token = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.delete_user_tokens = AsyncMock()
    repo.get = AsyncMock()
    repo.get_by = AsyncMock()

    return repo


@pytest.fixture
def mock_user_repo(mock_async_session):
    """Мок репозитория пользователей."""
    from app.repositories import UserRepository

    repo = MagicMock(spec=UserRepository)
    repo.session = mock_async_session

    repo.get_by_email = AsyncMock()
    repo.get = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.update_activity = AsyncMock()
    repo.exists_by = AsyncMock()

    return repo


@pytest.fixture
def mock_user_service(mock_async_session, mock_user_repo):
    """Мок сервиса пользователей."""
    from app.services.user import UserService

    service = MagicMock(spec=UserService)
    service.session = mock_async_session
    service.repo = mock_user_repo

    service.get_user_by_email = AsyncMock()
    service.get_user_by_id = AsyncMock()
    service.create_user = AsyncMock()
    service.update_user = AsyncMock()
    service.delete_user = AsyncMock()
    service.update_user_activity = AsyncMock()

    return service


@pytest.fixture
def mock_security_service():
    """Мок сервиса безопасности."""
    from app.core.security import SecurityService

    service = MagicMock(spec=SecurityService)

    service.get_password_hash = Mock()
    service.verify_password = Mock()
    service.create_access_token = Mock()
    service.create_refresh_token = Mock()
    service.verify_token = Mock()
    service.is_token_expired = Mock()

    return service


@pytest.fixture
def mock_db_user():
    """Мок SQLAlchemy модели User."""
    user = MagicMock()
    user.id = 1
    user.email = 'test@example.com'
    user.password_hash = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'
    user.role = UserRole.USER
    user.is_active = True
    user.created_at = None
    user.last_active_at = None
    user.total_active_time = 0
    user.status = 'active'

    return user


@pytest.fixture
def mock_db_token():
    """Мок SQLAlchemy модели RefreshToken."""
    token = MagicMock()
    token.id = 100
    token.user_id = 1
    token.token = 'refresh.token.value'
    token.expires_at = 9999999999

    return token
