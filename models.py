from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Menu(Base):
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("menus.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    has_image: Mapped[bool] = mapped_column(Boolean, server_default="0", default=False)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # 明確定義父子關聯
    children: Mapped[list["Menu"]] = relationship("Menu", back_populates="parent", cascade="all, delete-orphan")
    parent: Mapped["Menu"] = relationship("Menu", back_populates="children", remote_side=[id])

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_zh: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    sort_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1", default=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)
    name_zh: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(100), nullable=True)
    benefits: Mapped[str | None] = mapped_column(Text, nullable=True)
    volume_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    price_rm: Mapped[float | None] = mapped_column(Float, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="1", default=True)
    category: Mapped["Category"] = relationship(back_populates="products")

class Physician(Base):
    __tablename__ = "physicians"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False)
    education: Mapped[str | None] = mapped_column(String(100), nullable=True)
    specialties_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    portrait_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
