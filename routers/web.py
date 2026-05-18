from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, selectinload
from database import SessionLocal
import models
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_base_menus(db: Session):
    return db.query(models.Menu).options(selectinload(models.Menu.children)).filter(models.Menu.level == 1).order_by(models.Menu.sort_order).all()

@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    menus = get_base_menus(db)
    return templates.TemplateResponse(request, "index.html", {"menus": menus})

@router.get("/about")
async def about(request: Request, db: Session = Depends(get_db)):
    menus = get_base_menus(db)
    return templates.TemplateResponse(request, "about.html", {"menus": menus})

import json

@router.get("/team")
async def team(request: Request, db: Session = Depends(get_db)):
    menus = get_base_menus(db)
    physicians = db.query(models.Physician).all()
    
    for p in physicians:
        if p.specialties_json:
            try:
                p.specialties = json.loads(p.specialties_json)
            except:
                p.specialties = []
        else:
            p.specialties = []
            
    return templates.TemplateResponse(request, "team.html", {"menus": menus, "physicians": physicians})

@router.get("/contact")
async def contact(request: Request, db: Session = Depends(get_db)):
    menus = get_base_menus(db)
    return templates.TemplateResponse(request, "contact.html", {"menus": menus})

@router.get("/products")
async def products(request: Request, db: Session = Depends(get_db)):
    menus = get_base_menus(db)
    categories = db.query(models.Category).filter(models.Category.is_active == True).order_by(models.Category.sort_order).all()
    products = db.query(models.Product).filter(models.Product.is_active == True).all()
    return templates.TemplateResponse(request, "products.html", {
        "menus": menus, 
        "categories": categories,
        "products": products
    })
