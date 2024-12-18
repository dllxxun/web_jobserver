from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str
    company: str
    location: str
    salary_range: Optional[str]
    requirements: List[str]

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class NotificationSettings(BaseModel):
    email_notifications: bool
    push_notifications: bool
    notification_types: List[str]
