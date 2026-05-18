from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from typing import Optional
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter(prefix="/htmx")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products")
async def filter_products(
    request: Request, 
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Product).filter(models.Product.is_active == True)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    
    products = query.all()
    return templates.TemplateResponse(request, "partials/product_grid.html", {
        "products": products
    })
