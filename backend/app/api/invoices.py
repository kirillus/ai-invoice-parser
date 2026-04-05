import uuid
import os
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import get_settings
from app.models.invoices import UploadInvoiceResponse


router = APIRouter()
settings = get_settings()

# temporal solution before move to the database
invoice_store: dict[str, dict] = {}


async def upload_invoice(file: UploadFile = File(...)) -> UploadInvoiceResponse:
  """ Upload an invoice file to the server for processing """
  # 1 validate file extension
  ext = file.filename.split(".")[-1].lower() if file.filename else ""
  if ext not in settings.ALLOWED_FILE_EXTENSIONS:
    raise HTTPException(status_code=400,
      detail=f"Unsupported file extension. Allowed extensions: {', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
    )

  # 2 read file and check max size
  contents = await file.read()
  file_size_mb = len(contents) / (1024 * 1024)
  if (file_size_mb > settings.MAX_FILE_SIZE_MB):
    raise HTTPException(status_code=400,
      detail=f"File too large. Maxium size is {settings.MAX_FILE_SIZE_MB} MB"
    )

  # save file to disk
  os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
  invoice_id = str(uuid.uuid4()
  file_path = os.path.join(settings.UPLOAD_DIR, f"{invoice_id}.{ext}")

  with open(file_path, "wb") as f:
    f.write(contents)

  
  # store metadate
  # without parsing yet
  now = datetime.utcnow()
  invoice_store[invoice_id] = {
    "id": invoice_id,
    "file_path": file.filename,
    "status": "uploaded",
    "parsed_data": None,
    "created_at": now,
    "updated_at": now
  }

  return {
    "id":       invoice_id,
    "filename":  file.filename,
    "status":   "uploaded"
  }