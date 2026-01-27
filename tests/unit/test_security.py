from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from app.core.exceptions import AuthenticationError
from app.core.security import SecurityService
from app.schemas import UserRole, UserSchema


class TestSecurityService:
    """Тесты для SecurityService."""

    def test_get_password_hash(self):
        """Тест хэширования пароля."""
        password = 'test_password'
        hashed = SecurityService.get_password_hash(password)

        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Тест проверки правильного пароля."""
        password = 'test_password'
        hashed = SecurityService.get_password_hash(password)

        assert SecurityService.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Тест проверки неправильного пароля."""
        password = 'test_password'
        wrong_password = 'wrong_password'
        hashed = SecurityService.get_password_hash(password)

        assert SecurityService.verify_password(wrong_password, hashed) is False

    def test_edge_case_special_characters(self):
        """Тест с паролем из спецсимволов."""
        special_password = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
        hashed = SecurityService.get_password_hash(special_password)

        assert SecurityService.verify_password(special_password, hashed) is True

    def test_create_access_token(self):
        """Тест создания access токена."""
        user = UserSchema(id=1, email='test@example.com', role=UserRole.USER)
        token = SecurityService.create_access_token(user)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self):
        """Тест создания refresh токена."""
        user = UserSchema(id=1, email='test@example.com', role=UserRole.USER)
        token = SecurityService.create_refresh_token(user)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_valid_token(self):
        """Тест верификации валидного токена."""
        user = UserSchema(id=1, email='test@example.com', role=UserRole.USER)
        token = SecurityService.create_access_token(user)
        payload = SecurityService.verify_token(token)

        assert payload['sub'] == '1'
        assert payload['role'] == 'user'
        assert payload['type'] == 'access'

    def test_verify_expired_token(self):
        """Тест верификации истекшего токена."""
        with patch('app.core.security.s') as mock_settings:
            mock_settings.JWT_SECRET = 'test_secret'
            mock_settings.JWT_ALGORITHM = 'HS256'
            mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = -1  # Истекший токен

            user = UserSchema(id=1, email='test@example.com', role=UserRole.USER)
            token = SecurityService.create_access_token(user)

            with pytest.raises(AuthenticationError, match='Токен устарел'):
                SecurityService.verify_token(token)

    def test_verify_invalid_token(self):
        """Тест верификации невалидного токена."""
        invalid_token = 'invalid.token.string'

        with pytest.raises(AuthenticationError, match='Некорректный токен'):
            SecurityService.verify_token(invalid_token)

    def test_is_token_expired_false(self):
        """Тест проверки неистекшего токена."""
        future_time = datetime.now(UTC) + timedelta(days=1)
        expires_at = int(future_time.timestamp())

        assert SecurityService.is_token_expired(expires_at) is False

    def test_is_token_expired_true(self):
        """Тест проверки истекшего токена."""
        past_time = datetime.now(UTC) - timedelta(days=1)
        expires_at = int(past_time.timestamp())

        assert SecurityService.is_token_expired(expires_at) is True

    def test_token_types_different(self):
        """Тест что access и refresh токены разные."""
        user = UserSchema(id=1, email='test@example.com', role=UserRole.USER)

        access_token = SecurityService.create_access_token(user)
        refresh_token = SecurityService.create_refresh_token(user)

        assert access_token != refresh_token

        access_payload = SecurityService.verify_token(access_token)
        refresh_payload = SecurityService.verify_token(refresh_token)

        assert access_payload['type'] == 'access'
        assert refresh_payload['type'] == 'refresh'
        assert 'login' in access_payload
        assert 'login' not in refresh_payload
