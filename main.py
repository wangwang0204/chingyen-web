import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import web, htmx

# Robust BASE_DIR detection for Vercel vs Local
current_file = Path(__file__).resolve()
if current_file.parent.name == 'api':
    BASE_DIR = current_file.parent.parent
else:
    BASE_DIR = current_file.parent

app = FastAPI(title="Chingyen Digital Catalog MVP")

# Mount static files with absolute path
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(web.router)
app.include_router(htmx.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
