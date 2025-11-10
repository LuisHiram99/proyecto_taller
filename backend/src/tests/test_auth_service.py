from sys import exc_info
import pytest
from datetime import timedelta
from sqlalchemy import select
from db import models
from auth import auth
from jose import JWTError, jwt

class TestAuthService:
    def test_verify_password(self):
        """Test password hashing and verification"""
        plain_password = "mysecretpassword"
        hashed_password = auth.pwd_context.hash(plain_password)
        assert auth.pwd_context.verify(plain_password, hashed_password)
        assert not auth.pwd_context.verify("wrongpassword", hashed_password)

    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """Test user creation with password hashing"""
        user_data = auth.CreateUserRequest(
            first_name="Test",
            last_name="User",
            email="test@mail.com",
            password="securepassword"
        )
        response = await auth.create_user(user_data, db_session)
        assert response.first_name == "Test"
        assert response.email == "test@mail.com"
        
        # Verify password is hashed
        result = await db_session.execute(
            select(models.User).where(models.User.email == "test@mail.com")
        )
        db_user = result.scalar_one()
        assert auth.pwd_context.verify("securepassword", db_user.hashed_password)

    async def test_create_user_duplicate_email(self, db_session):
        """Test that creating a user with a duplicate email raises an exception"""
        user_data = auth.CreateUserRequest(
            first_name="Test",
            last_name="User",
            email="test@mail.com",
            password="securepassword"
        )
        created_user = await auth.create_user(user_data, db_session)
        assert created_user.first_name == "Test"
        assert created_user.email == "test@mail.com"

        with pytest.raises(auth.HTTPException) as exc_info:
            await auth.create_user(user_data, db_session)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Email already registered"

    @pytest.mark.asyncio
    async def test_create_invalid_user(self, db_session):
        """Test that creating a user with invalid data raises an exception"""
        user_data = auth.CreateUserRequest(
            first_name="",
            last_name="User",
            email="invalidemail",
            password="short"
        )
        with pytest.raises(Exception):
            await auth.create_user(user_data, db_session)

    @pytest.mark.asyncio
    async def test_login_for_access_token(self, db_session):
        """Test user authentication and JWT token generation"""
        # First, create a user
        user_data = auth.CreateUserRequest(
            first_name="Test",
            last_name="User",
            email="testlogin@mail.com",
            password="securepassword"
        )
        created_user = await auth.create_user(user_data, db_session)
        assert created_user.first_name == "Test"
        assert created_user.email == "testlogin@mail.com"
        
        # Now test authentication
        authenticated_user = await auth.authenticate_user(db_session, "testlogin@mail.com", "securepassword")
        assert authenticated_user is not False
        assert authenticated_user.email == "testlogin@mail.com"
        
        # Test token creation
        token = auth.create_access_token(
            authenticated_user.email,
            authenticated_user.user_id,
            authenticated_user.token_version,
            timedelta(minutes=30)
        )
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify token
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        assert payload["sub"] == "testlogin@mail.com"
        assert payload["user_id"] == created_user.user_id