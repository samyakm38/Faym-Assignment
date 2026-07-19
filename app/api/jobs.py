from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.sale_service import SaleService



router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

@router.post("/process-advances")
def process_advances(
    db: Session = Depends(get_db),
):
    service = SaleService(db)

    processed = service.process_pending_advances()
    return {
        "processed_sales": processed,
    }
    