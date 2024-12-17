from fastapi import APIRouter
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/statistics")
async def get_statistics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """채용 통계 조회"""
    pass
