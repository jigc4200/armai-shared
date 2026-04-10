"""Encryption module for API keys using Fernet (AES-256)."""

import os
import logging
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger(__name__)

# Global Fernet instance (initialized on first use)
_fernet: Optional[Fernet] = None


def _get_fernet() -> Fernet:
    """Get or create Fernet instance with encryption key from environment."""
    global _fernet
    
    if _fernet is None:
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError(
                "ENCRYPTION_KEY environment variable is required. "
                "Generate one with: python -c \"from cryptography.fernet import Fernet; "
                "print(Fernet.generate_key().decode())\""
            )
        
        # Ensure key is properly formatted
        if isinstance(key, str):
            key = key.encode()
        
        _fernet = Fernet(key)
        logger.info("Fernet encryption initialized")
    
    return _fernet


def validate_encryption_key() -> bool:
    """
    Validate that ENCRYPTION_KEY is properly configured.
    
    Returns:
        True if encryption key is valid
        
    Raises:
        ValueError: If ENCRYPTION_KEY is missing or invalid
    """
    try:
        _get_fernet()
        return True
    except ValueError as e:
        logger.error(f"Encryption key validation failed: {e}")
        raise


def encrypt_api_key(plain_text: str) -> str:
    """
    Encrypt an API key using Fernet.
    
    Args:
        plain_text: Plain text API key to encrypt
        
    Returns:
        Encrypted API key as base64-encoded string
        
    Raises:
        ValueError: If encryption fails
    """
    if not plain_text:
        raise ValueError("Cannot encrypt empty API key")
    
    try:
        fernet = _get_fernet()
        encrypted = fernet.encrypt(plain_text.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Failed to encrypt API key: {e}")
        raise ValueError(f"Encryption failed: {e}")


def decrypt_api_key(encrypted_text: str) -> str:
    """
    Decrypt an API key using Fernet.
    
    Args:
        encrypted_text: Encrypted API key (base64-encoded)
        
    Returns:
        Decrypted plain text API key
        
    Raises:
        ValueError: If decryption fails (e.g., invalid token or wrong key)
    """
    if not encrypted_text:
        raise ValueError("Cannot decrypt empty API key")
    
    try:
        fernet = _get_fernet()
        decrypted = fernet.decrypt(encrypted_text.encode())
        return decrypted.decode()
    except InvalidToken:
        logger.error("Failed to decrypt API key: Invalid token (wrong encryption key or corrupted data)")
        raise ValueError("Invalid encryption token - check ENCRYPTION_KEY matches")
    except Exception as e:
        logger.error(f"Failed to decrypt API key: {e}")
        raise ValueError(f"Decryption failed: {e}")


def rotate_key(old_key: str, new_key: str, encrypted_data: str) -> str:
    """
    Re-encrypt data with a new key.
    
    Args:
        old_key: Current encryption key
        new_key: New encryption key to use
        encrypted_data: Data encrypted with old_key
        
    Returns:
        Data re-encrypted with new_key
    """
    # Decrypt with old key
    old_fernet = Fernet(old_key.encode() if isinstance(old_key, str) else old_key)
    decrypted = old_fernet.decrypt(encrypted_data.encode())
    
    # Re-encrypt with new key
    new_fernet = Fernet(new_key.encode() if isinstance(new_key, str) else new_key)
    encrypted = new_fernet.encrypt(decrypted)
    
    return encrypted.decode()
