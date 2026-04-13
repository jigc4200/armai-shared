"""Shared utilities for ARMAI platform."""

from .channel_contracts import InboundMessage, OutboundMessage, ChannelType
from .crypto import (
    encrypt,
    decrypt,
    encrypt_api_key,
    decrypt_api_key,
    validate_encryption_key,
    rotate_key,
)
from .constants import AgentTool, ALL_AGENT_TOOLS

__all__ = [
    # channel_contracts
    "InboundMessage",
    "OutboundMessage",
    "ChannelType",
    # crypto
    "encrypt",
    "decrypt",
    "encrypt_api_key",
    "decrypt_api_key",
    "validate_encryption_key",
    "rotate_key",
    # constants
    "AgentTool",
    "ALL_AGENT_TOOLS",
]
