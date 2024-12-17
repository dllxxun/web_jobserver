from fastapi import APIRouter, Query
from typing import Optional, List

router = APIRouter()

@router.post("/bookmarks/{job_id}")
async def add_bookmark(job_id: int):
    """북마크 추가"""
    pass

@router.get("/bookmarks")
async def get_bookmarks(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100)
):
    """북마크 목록 조회"""
    pass

@router.delete("/bookmarks/{bookmark_id}")
async def delete_bookmark(bookmark_id: int):
    """북마크 삭제"""
    pass
