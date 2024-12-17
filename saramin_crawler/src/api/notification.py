from fastapi import APIRouter, Query
from typing import List
from .models import NotificationSettings

router = APIRouter()


@router.post("/notifications/settings")
async def update_notification_settings(settings: NotificationSettings):
    """알림 설정 업데이트"""
    pass

@router.get("/notifications")
async def get_notifications(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100)
):
    """알림 목록 조회"""
    pass
