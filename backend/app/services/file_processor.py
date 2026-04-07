import io
from pathlib import Path
from PIL import Image


try:
  import pytesseract
  HAS_TESSERACT = True
except ImportError:
  HAS_TESSERACT = False


try:
  from pdf2image import convert_from_bytes
  HAS_PDF2IMAGE = True
except ImportError:
  HAS_PDF2IMAGE = False


async def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
  ext = Path(filename).suffix.lower()

  if ext == ".pdf":
    return await extract_from_pdf(file_bytes, filename)
  elif ext in (".jpg", ".jpeg", ".png", ".tiff"):
    return await extract_from_image(file_bytes, filename)
  else:
    raise ValueError(f"Unsupported file extension: {ext}")



async def extract_from_pdf(file_bytes: bytes, filename: str) -> str:
  if not HAS_PDF2IMAGE or not HAS_TESSERACT:
    raise RuntimeError("Install pdf2image and pytesseract to extract text from PDF files")

  images = convert_from_bytes(file_bytes)
  text_parts = []

  for page in images:
    text = pytesseract.image_to_string(page)
    text_parts.append(text)
    
  return "\n\n".join(text_parts)


async def extract_from_image(file_bytes: bytes, filename: str) -> str:
  if not HAS_TESSERACT:
    raise RuntimeError("Install pytesseract to extract text from image files")


  image = Image.open(io.BytesIO(file_bytes))
  text = pytesseract.image_to_string(image)

  return text


