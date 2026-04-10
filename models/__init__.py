"""Shared Pydantic models for Project X."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message role enum."""

    HUMAN = "human"
    ASSISTANT = "assistant"


class WebhookMessage(BaseModel):
    """Message received from WhatsApp webhook."""

    tenant_id: str = Field(default="00000000-0000-0000-0000-000000000001")
    phone_number: str
    message: str
    message_id: str
    timestamp: str
    conversation_id: Optional[str] = None


class ProcessedMessage(BaseModel):
    """Message processed by the worker."""

    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime


class WhatsAppPayload(BaseModel):
    """Meta WhatsApp webhook payload structure."""

    object: str
    entry: list[dict]