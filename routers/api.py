import os
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api")

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
MODEL_ID = "google/gemini-2.0-flash-lite-preview-02-05"

# 預植入的店內資訊，模擬「打開 DB 看」
STORE_INFO = """
店名：金燕 (Chingyen) 中藥行
產品：
1. 天池雪蛤膏 (RM 68.00)
2. 西藏冬蟲夏草王 (RM 1588.00)
3. 印尼金絲花燕 (RM 118.00) - 美容養顏, 潤肺止咳
4. 印尼白洞燕 (RM 118.00) - 美容養顏, 潤肺止咳
5. 印尼珍珠燕盞 (RM 3188.00) - 潤肺止咳
6. 有機小米 (Millet)
7. 福建白蓮子 (Lotus Seed)
8. 凍乾枸杞子 (Gojiberry)
9. 正紋黨參 (Dangshen)

醫師團隊：
1. 顏成福 (中醫師)：26年經驗，專長：兒科、看體質把脈、調理氣血。
2. 林美玉 (中醫師)：16年經驗，專長：婦科調理、藥膳搭配、月子調理。
"""

SYSTEM_PROMPT = f"""
你是一位金燕中藥行的專業中醫客服。請用繁體中文、親切的語氣回答。
為了確保系統穩定，你的回答必須極度精簡，絕對不能超過 50 個字。
你可以參考以下店內資訊來回答客戶：
{STORE_INFO}
"""

@router.post("/chat", response_class=HTMLResponse)
async def chat_endpoint(request: Request, message: str = Form(...)):
    if not OPEN_ROUTER_API_KEY:
        return "<div class='bg-red-100 p-3 rounded-lg text-red-700 text-sm mb-2'>錯誤：未設定 API Key</div>"

    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    # 使用者訊息氣泡
    user_bubble = f"""
    <div class="flex justify-end mb-4 animate-in fade-in slide-in-from-right-2 duration-300">
        <div class="bg-brand-red text-white p-3 rounded-2xl rounded-tr-none max-w-[80%] shadow-sm">
            <p class="text-sm">{message}</p>
        </div>
    </div>
    """

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=8.0 # 嚴格控制在 10s 內
            )
            response.raise_for_status()
            data = response.json()
            bot_reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = "抱歉，我現在有點忙，請稍後再問我，或直接撥打我們的電話諮詢。"

    # 機器人回覆氣泡
    bot_bubble = f"""
    <div class="flex justify-start mb-4 animate-in fade-in slide-in-from-left-2 duration-300">
        <div class="bg-brand-beige border border-brand-khaki text-brand-gray p-3 rounded-2xl rounded-tl-none max-w-[80%] shadow-sm">
            <p class="text-sm">{bot_reply}</p>
        </div>
    </div>
    """

    return user_bubble + bot_bubble
