from pydantic import ConfigDict, BaseModel
from typing import Optional

class MenuSchema(BaseModel):
    id: int
    parent_id: Optional[int] = None
    title: str
    level: int
    sort_order: int
    has_image: bool
    image_path: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class CategorySchema(BaseModel):
    id: int
    name_zh: str
    slug: str
    sort_order: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class ProductSchema(BaseModel):
    id: int
    category_id: int
    sku: Optional[str] = None
    name_zh: str
    name_en: Optional[str] = None
    benefits: Optional[str] = None
    volume_size: Optional[str] = None
    price_rm: Optional[float] = None
    image_path: Optional[str] = None
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class PhysicianSchema(BaseModel):
    id: int
    name: str
    title: str
    experience_years: int
    education: Optional[str] = None
    specialties_json: Optional[str] = None
    portrait_path: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
