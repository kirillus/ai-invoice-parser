import asyncio
import sys
from pathlib import Path

from app.services.file_processor import extract_text_from_file as extract_text


def resolve_pdf_path() -> Path:
  if len(sys.argv) > 1:
    candidate = Path(sys.argv[1]).expanduser()
    return candidate if candidate.is_absolute() else (Path.cwd() / candidate)

  uploads_dir = Path("uploads")
  pdfs = sorted(uploads_dir.glob("*.pdf"))
  if pdfs:
    return pdfs[0]

  return Path("test.pdf")


async def main():
  pdf_path = resolve_pdf_path()
  if not pdf_path.exists():
    raise FileNotFoundError(
      f"PDF not found: {pdf_path}. Pass a path, e.g. `python test_osr.py uploads/your.pdf`."
    )

  with open(pdf_path, "rb") as f:
    text = await extract_text(f.read(), pdf_path.name)
    print(text)

if __name__ == "__main__":
  asyncio.run(main())