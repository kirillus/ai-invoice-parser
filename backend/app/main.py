from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.invoices import router as invoices_router


settings = get_settings()

app = FastAPI(
  title=settings.APP_NAME,
  version=settings.APP_VERSION
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(
  invoices_router,
  prefix=f"{settings.API_V1_PREFIX}/invoices",
  tags=[]"invoices"]
)


@app.get("/health")
async def health():
  return {"status": "healthy", "version": settings.APP_VERSION}
