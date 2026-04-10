"""Shared channel contracts — normalized message types for all inbound/outbound channels.

All services (api-gateway, worker-whatsapp, channel-gateway, worker-langchain)
MUST use these types when publishing to or consuming from Redis.  This ensures the
worker is channel-agnostic: it only sees an InboundMessage regardless of origin.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ChannelType(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    VOICE = "voice"


class InboundMessage(BaseModel):
    """Normalized representation of a message arriving from any channel."""

    channel: ChannelType
    tenant_id: str
    from_: str                       # phone number, email address, or caller_id
    body: str                        # message text or STT transcription
    subject: Optional[str] = None    # email only
    thread_id: Optional[str] = None  # email Message-Id or voice CallSid
    raw: Optional[dict] = None       # original provider payload (for debugging)


class OutboundMessage(BaseModel):
    """Normalized representation of a message to be sent through any channel."""

    channel: ChannelType
    tenant_id: str
    to: str
    body: str
    subject: Optional[str] = None   # email only
    thread_id: Optional[str] = None # reply to existing email thread or call
