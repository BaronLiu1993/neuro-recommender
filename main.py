from fastapi import FastAPI
from router.analysis_router import router as analysis_router
from router.auth_router import router as auth_router

app = FastAPI()
app.include_router(analysis_router)
app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
