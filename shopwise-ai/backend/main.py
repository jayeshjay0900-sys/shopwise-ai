from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router
from backend.config import settings

app = FastAPI(title="ShopWise AI", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

frontend_dist = Path(settings.frontend_dist)
if frontend_dist.exists():
    assets = frontend_dist / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")


@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    return FileResponse(frontend_dist / "index.html")


@app.get("/{path:path}", include_in_schema=False)
async def spa_fallback(path: str) -> FileResponse:
    requested = frontend_dist / path
    if requested.is_file():
        return FileResponse(requested)
    return FileResponse(frontend_dist / "index.html")
