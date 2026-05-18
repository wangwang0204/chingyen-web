from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import web, htmx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Chingyen Digital Catalog MVP")

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Include routers
app.include_router(web.router)
app.include_router(htmx.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
