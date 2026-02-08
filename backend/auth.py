from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings

# Password hashing with Argon2id (with Bcrypt backward compatibility)
# Argon2id is the recommended password hashing algorithm by OWASP
# It provides better security than bcrypt and has no password length limitations
# We keep bcrypt in the list for backward compatibility with existing passwords
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # Argon2 first (preferred), Bcrypt for legacy
    deprecated=["bcrypt"],  # Mark bcrypt as deprecated - will auto-upgrade on verify
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,  # 3 iterations
    argon2__parallelism=4,  # 4 parallel threads
    argon2__hash_len=32,  # 32 bytes hash length
    bcrypt__default_rounds=12,  # For legacy bcrypt passwords
    bcrypt__truncate_error=False,  # Auto-truncate passwords > 72 bytes (fixes passlib init error)
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2id
    
    Args:
        password: Plain text password to hash
    
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing user data to encode
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token
    
    Args:
        data: Dictionary containing user data to encode
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token
    
    Args:
        token: JWT token string to decode
    
    Returns:
        Decoded payload dictionary if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Verify it's an access token
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None


def decode_refresh_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT refresh token
    
    Args:
        token: JWT refresh token string to decode
    
    Returns:
        Decoded payload dictionary if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None

