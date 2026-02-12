"""
Security utilities for JWT authentication
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import os

try:
    import jwt
except ImportError:
    jwt = None

from app.config import settings


class SecurityUtils:
    """Security utilities for authentication and authorization"""
    
    # Use environment variable or fallback to default (should be set in production)
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Dictionary of data to encode in the token
            expires_delta: Optional expiration time delta
            
        Returns:
            Encoded JWT token string
            
        Raises:
            RuntimeError: If PyJWT is not installed
        """
        if jwt is None:
            raise RuntimeError("PyJWT is not installed. Run: pip install PyJWT")
        
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=SecurityUtils.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow()
        })
        
        encoded_jwt = jwt.encode(
            to_encode, 
            SecurityUtils.SECRET_KEY, 
            algorithm=SecurityUtils.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        Verify JWT token and return decoded data.
        
        Args:
            token: JWT token string to verify
            
        Returns:
            Decoded token data as dictionary
            
        Raises:
            jwt.ExpiredSignatureError: If token has expired
            jwt.InvalidTokenError: If token is invalid
            RuntimeError: If PyJWT is not installed
        """
        if jwt is None:
            raise RuntimeError("PyJWT is not installed. Run: pip install PyJWT")
        
        try:
            decoded = jwt.decode(
                token,
                SecurityUtils.SECRET_KEY,
                algorithms=[SecurityUtils.ALGORITHM]
            )
            return decoded
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token")
