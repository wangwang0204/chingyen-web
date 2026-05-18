# 金燕 (Chingyen) 數位型錄 MVP - AI 開發技術規格書

## 1. 專案概述與技術架構 (Project Overview & Tech Stack)

* **目標**：開發一個展示中醫醫療團隊與中藥產品目錄的官方網站，主打「新客獲取」與「SEO 友善」。
* **後端框架**：FastAPI (Python >= 3.9)
* **前端架構**：Jinja2 (SSR), HTMX (局部渲染), Alpine.js (輕量級狀態管理)
* **資料庫**：SQLite + SQLAlchemy 2.0 (嚴格採用 Declarative Mapping 與 Type Hinting)
* **CSS 設計**：自訂 CSS，遵循品牌色系（`--color-red: #A33327`, `--color-khaki: #D9C5A0`, `--color-beige: #F5EFE6`, `--color-gold: #C5A059`, `--color-light-green: #A3B899`）。
* **核心規範**：
* 遵循 PEP 585，**絕對禁止**使用 `typing.List` 或 `typing.Dict`，請直接使用內建的 `list` 與 `dict` 進行泛型標註。
* 程式碼需具備完整 Docstrings 與 Pydantic Schemas 驗證。
* 選單與分類結構需由資料庫動態驅動。



---

## 2. 目錄結構規範 (Directory Structure)

請 Agent 嚴格依照以下結構建立檔案：

```text
chingyen_mvp/
├── main.py                  # FastAPI 應用程式入口與路由註冊
├── database.py              # SQLite 連線引擎 (sqlite:///./chingyen.db) 與 SessionLocal
├── models.py                # SQLAlchemy 2.0 實體定義
├── schemas.py               # Pydantic 驗證模型
├── init_db.py               # 資料庫初始化與 SQL Seed 腳本
├── routers/                 
│   ├── web.py               # 處理 Jinja2 頁面渲染路由
│   └── htmx.py              # 處理 HTMX 局部請求路由 (回傳 partial HTML)
├── templates/               
│   ├── base.html            # 基底樣板 (匯入 Alpine.js 與 HTMX CDN)
│   ├── index.html           # 首頁
│   ├── about.html           # 關於我們
│   ├── team.html            # 醫療團隊
│   ├── products.html        # 產品目錄主頁
│   └── partials/            
│       └── product_grid.html # 供 HTMX 呼叫的商品網格元件
└── static/                  
    ├── css/style.css
    ├── js/main.js
    └── images/              # brand/, store/, team/, products/

```

---

## 3. SQLAlchemy 2.0 資料表定義 (`models.py`)

請 Agent 實作以下宣告式模型：

```python
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
    has_image: Mapped[bool] = mapped_column(Boolean, default=False)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    children: Mapped[list["Menu"]] = relationship("Menu", backref="parent", remote_side=[id])

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_zh: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    sort_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
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
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
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

```

---

## 4. 核心 Seed Data (SQL Insert 指令)

請 Agent 在 `init_db.py` 中建立資料表後，執行以下原生 SQL 語句完成資料庫初始化。

### 4.1 選單架構 (Menus)

```sql
-- 主選單
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (1, NULL, '首頁', 1, 1);
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (11, NULL, '公司簡介', 1, 2);
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (17, NULL, '產品資訊', 1, 3);
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (37, NULL, '聯絡我們', 1, 4);

-- 首頁子區塊
INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (2, 1, 'Logo', 2, 1, 1);
INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (4, 1, '主視覺', 2, 2, 1);
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (5, 1, '產品分類/服務項目', 2, 3);

-- 公司簡介子區塊
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (12, 11, '公司簡介', 2, 1);
INSERT INTO menus (id, parent_id, title, level, sort_order) VALUES (14, 11, '經營理念', 2, 2);
INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (16, 11, '執照認證', 2, 3, 1);

```

### 4.2 產品分類與目錄 (Categories & Products)

```sql
-- 分類 (隱藏目前沒有詳細資料的分類)
INSERT INTO categories (id, name_zh, slug, sort_order, is_active) VALUES (1, '漢方', 'herbal', 1, 1);
INSERT INTO categories (id, name_zh, slug, sort_order, is_active) VALUES (2, '涼茶 & 糖水', 'tea-dessert', 2, 0);
INSERT INTO categories (id, name_zh, slug, sort_order, is_active) VALUES (3, '酒', 'wine', 3, 0);

-- 商品資料
INSERT INTO products (id, category_id, sku, name_zh, name_en, benefits, volume_size, price_rm, image_path, is_active) VALUES 
(1, 1, 'HERB-001', '天池雪蛤膏', NULL, NULL, NULL, 68.00, '/static/images/products/prod-snow-lotus.jpg', 1),
(2, 1, 'HERB-002', '西藏冬虫夏草王', NULL, NULL, '18.75g', 1588.00, '/static/images/products/prod-cordyceps.jpg', 1),
(3, 1, 'HERB-003', '印尼金丝花燕', NULL, '美容养颜, 润肺止咳, 养阴润燥', NULL, 118.00, '/static/images/products/prod-golden-birdnest.jpg', 1),
(4, 1, 'HERB-004', '印尼白洞燕', NULL, '美容养颜, 润肺止咳, 养阴', NULL, 118.00, '/static/images/products/prod-white-birdnest.jpg', 1),
(5, 1, 'HERB-005', '印尼珍珠燕盏', NULL, '美容养颜, 润肺止咳, 养阴润燥', '500g', 3188.00, '/static/images/products/prod-pearl-birdnest.jpg', 1),
(6, 1, 'HERB-006', '有机小米', 'Organic Millet', NULL, NULL, NULL, '/static/images/products/prod-millet.jpg', 1),
(7, 1, 'HERB-007', '福建白莲子', 'Hokkien Lotus Seed', NULL, '1kg', 16.80, '/static/images/products/prod-lotus-seed.jpg', 1),
(8, 1, 'HERB-008', '冻干枸杞子', 'Gojiberry', NULL, NULL, NULL, '/static/images/products/prod-goji.jpg', 1),
(9, 1, 'HERB-009', '正纹党参', NULL, NULL, '500g', 150.00, '/static/images/products/prod-dangshen.jpg', 1);

```

### 4.3 醫師團隊 (Physicians)

```sql
INSERT INTO physicians (id, name, title, experience_years, education, specialties_json, portrait_path) VALUES 
(1, '颜成福', '中医师', 26, '吉隆坡中医学院', '["儿科", "看体质把脉", "调理气血"]', '/static/images/team/doc-yan.jpg'),
(2, '林美玉', '中医师', 16, '吉隆坡中医学院', '["妇科调理", "养生与调理", "中药与药膳搭配", "中医月子调理"]', '/static/images/team/doc-lin.jpg');

```

---

## 5. UI 互動實作要求 (Actionable Tasks for Agent)

1. **導覽列 (Alpine.js)**：在 `base.html` 中實作 Responsive Navbar。使用 `x-data="{ open: false }"` 控制手機版選單的展開與收合。
2. **產品過濾 (HTMX)**：在 `products.html` 頁面，為分類按鈕加入 `hx-get="/htmx/products?category_id=X"` 與 `hx-target="#product-grid"` 屬性。當使用者點擊分類時，後端 `routers/htmx.py` 只需透過 Jinja2 回傳 `partials/product_grid.html`，達成無刷新切換。
3. **依賴套件管理**：請產生 `requirements.txt`，務必包含 `fastapi`, `uvicorn`, `sqlalchemy`, `jinja2`, `pydantic`。