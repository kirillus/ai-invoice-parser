import json
import re
import anthropic
from app.core.config import get_settings
from app.models.invoices import ParsedInvoice, LineItem

settings = get_settings()


EXTRACTION_PROMT = """You are an invoice data extraction specialist.
Analyze the provided invoice text and extract structured data.

Return a JSON object with these fields:
- vendor_name: Company/person who issued the invoice
- vendor_address: Full address of the vendor
- invoice_number: Invoice/reference number
- invoice_date: Date issued (YYYY-MM-DD)
- due_date: Payment due date (YYYY-MM-DD)
- subtotal: Amount before tax
- tax: Tax amount
- total: Total amount due
- currency: Currency code (USD, EUR, CAD)
- line_items: Array with: description, quantity, unit_price, amount, confidence (0-1)
- confidence_scores: Object mapping each field to confidence (0-1)

For fields you can't find, set null with low confidence.
Return ONLY valid JSON, no markdown."""


def _parse_json_from_response(response_text: str) -> dict:
  candidates = [response_text.strip()]

  fenced = re.findall(r"```(?:json)?\s*([\s\S]*?)```", response_text, flags=re.IGNORECASE)
  candidates.extend(chunk.strip() for chunk in fenced if chunk.strip())

  start = response_text.find("{")
  end = response_text.rfind("}")
  if start != -1 and end != -1 and end > start:
    candidates.append(response_text[start : end + 1].strip())

  for candidate in candidates:
    if not candidate:
      continue
    try:
      return json.loads(candidate)
    except json.JSONDecodeError:
      continue

  raise ValueError("Failed to parse AI response as JSON")


async def parse_invoice_with_ai(text: str) -> ParsedInvoice:
  if not settings.ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not configured")

  client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
  model = settings.ANTHROPIC_MODEL

  try:
    message = await client.messages.create(
      model=model,
      max_tokens=2000,
      messages=[
        {"role": "user", "content": f"{EXTRACTION_PROMT}\n\nINVOICE TEXT:{text}"}
      ]
    )
  except anthropic.NotFoundError:
    models = await client.models.list(limit=20)
    available_ids = [m.id for m in models.data]
    if not available_ids:
      raise

    preferred = next((mid for mid in available_ids if "haiku" in mid.lower()), available_ids[0])
    message = await client.messages.create(
      model=preferred,
      max_tokens=2000,
      messages=[
        {"role": "user", "content": f"{EXTRACTION_PROMT}\n\nINVOICE TEXT:{text}"}
      ]
    )

  response_chunks = [getattr(block, "text", "") for block in message.content]
  response_text = "\n".join(chunk for chunk in response_chunks if chunk).strip()
  data = _parse_json_from_response(response_text)


  line_items = []
  for item in data.get("line_items", []):
    line_items.append(LineItem(
      description=item.get("description", ""),
      quantity=item.get("quantity", None),
      unit_price=item.get("unit_price", None),
      amount=item.get("amount", 0.0),
      confidence=item.get("confidence", 0.5)
    ))

  return ParsedInvoice(
    vendor_name=data.get("vendor_name", ""),
    vendor_address=data.get("vendor_address", ""),
    invoice_number=data.get("invoice_number", ""),
    invoice_date=data.get("invoice_date", None),
    due_date=data.get("due_date", None),
    subtotal=data.get("subtotal", 0.0),
    tax=data.get("tax", 0.0),
    total=data.get("total", 0.0),
    currency=data.get("currency", "USD"),
    line_items=line_items,
    raw_text=text,
    confidence_scores=data.get("confidence_scores", {})
  )

  


