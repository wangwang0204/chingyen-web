from sqlalchemy import text
from database import engine, SessionLocal
from models import Base

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as session:
        # --- 1. 完整選單架構 ---
        # 修正：確保 VALUES 的數量與欄位數量一致
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (1, NULL, '首頁', 1, 1, 0)"))
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (11, NULL, '公司簡介', 1, 2, 0)"))
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (17, NULL, '產品資訊', 1, 3, 0)"))
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (21, NULL, '能力優勢', 1, 4, 0)"))
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (31, NULL, '服務支援', 1, 5, 0)"))
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (41, NULL, '人力資源', 1, 6, 0)"))
        session.execute(text("INSERT INTO menus (id, parent_id, title, level, sort_order, has_image) VALUES (37, NULL, '聯絡我們', 1, 7, 0)"))

        # 子選單
        session.execute(text("INSERT INTO menus (parent_id, title, level, sort_order) VALUES (11, '公司簡介', 2, 1)"))
        session.execute(text("INSERT INTO menus (parent_id, title, level, sort_order) VALUES (11, '經營理念', 2, 2)"))
        session.execute(text("INSERT INTO menus (parent_id, title, level, sort_order) VALUES (17, '產品分類A', 2, 1)"))
        session.execute(text("INSERT INTO menus (parent_id, title, level, sort_order) VALUES (21, '品質政策', 2, 1)"))

        # --- 2. 產品分類 ---
        session.execute(text("INSERT INTO categories (id, name_zh, slug, sort_order, is_active) VALUES (1, '漢方', 'herbal', 1, 1)"))
        session.execute(text("INSERT INTO categories (id, name_zh, slug, sort_order, is_active) VALUES (2, '涼茶 & 糖水', 'tea-dessert', 2, 0)"))

        # --- 3. 完整產品資料 (9 樣) ---
        products = [
            (1, 1, 'HERB-001', '天池雪蛤膏', None, None, None, 68.00, '/static/images/products/prod-snow-lotus.jpg', 1),
            (2, 1, 'HERB-002', '西藏冬蟲夏草王', None, None, '18.75g', 1588.00, '/static/images/products/prod-cordyceps.jpg', 1),
            (3, 1, 'HERB-003', '印尼金絲花燕', None, '美容養顏, 潤肺止咳, 養陰潤燥', None, 118.00, '/static/images/products/prod-golden-birdnest.jpg', 1),
            (4, 1, 'HERB-004', '印尼白洞燕', None, '美容養顏, 潤肺止咳, 養陰', None, 118.00, '/static/images/products/prod-white-birdnest.jpg', 1),
            (5, 1, 'HERB-005', '印尼珍珠燕盞', None, '美容養顏, 潤肺止咳, 養陰潤燥', '500g', 3188.00, '/static/images/products/prod-pearl-birdnest.jpg', 1),
            (6, 1, 'HERB-006', '有機小米', 'Organic Millet', None, None, None, '/static/images/products/prod-millet.jpg', 1),
            (7, 1, 'HERB-007', '福建白蓮子', 'Hokkien Lotus Seed', None, '1kg', 16.80, '/static/images/products/prod-lotus-seed.jpg', 1),
            (8, 1, 'HERB-008', '凍乾枸杞子', 'Gojiberry', None, None, None, '/static/images/products/prod-goji.jpg', 1),
            (9, 1, 'HERB-009', '正紋黨參', None, None, '500g', 150.00, '/static/images/products/prod-dangshen.jpg', 1),
        ]
        
        for p in products:
            session.execute(text("""
                INSERT INTO products (id, category_id, sku, name_zh, name_en, benefits, volume_size, price_rm, image_path, is_active) 
                VALUES (:id, :cat, :sku, :zh, :en, :ben, :vol, :price, :img, :act)
            """), {"id": p[0], "cat": p[1], "sku": p[2], "zh": p[3], "en": p[4], "ben": p[5], "vol": p[6], "price": p[7], "img": p[8], "act": p[9]})

        # --- 4. 醫師團隊 ---
        session.execute(text("""
            INSERT INTO physicians (id, name, title, experience_years, education, specialties_json, portrait_path) VALUES 
            (1, '顏成福', '中醫師', 26, '吉隆坡中醫學院', '["兒科", "看體質把脈", "調理氣血"]', '/static/images/team/doc-yan.jpg'),
            (2, '林美玉', '中醫師', 16, '吉隆坡中醫學院', '["婦科調理", "養生與調理", "中藥與藥膳搭配", "中醫月子調理"]', '/static/images/team/doc-lin.jpg')
        """))
        
        session.commit()
        print("Database restored with full product list.")

if __name__ == "__main__":
    init_db()
