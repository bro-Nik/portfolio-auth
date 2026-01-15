from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoginSessionCreate(BaseModel):
    user_id: int
    refresh_token_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    platform: Optional[str] = None


class LoginSessionUpdate(BaseModel):
    ip_address: Optional[str] = None
    last_activity_at: Optional[datetime] = None


class LoginSessionResponse(BaseModel):
    id: int
    ip_address: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    platform: Optional[str] = None
    login_at: datetime
    last_activity_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
