from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum

class ExportFormat(str, Enum):
  CSV = "csv"
  JSON = "json"

class LineItem(BaseModel):
  """ Singles line on an invoice """
  description: str = Field(..., description="The description of the line item")
  quantity: float | None = None
  unit_price: float | None = None
  amount: float
  confidence: float = Field(ge=0.0, le=1.0, description="AI Confidence score for the line item")


""" Enum for currency """
class Currency(str, Enum):
  USD = "USD"
  CAD = "CAD"


class ParsedInvoice(BaseModel):
  """ All Data extracted from an invoice """
  vendor_name: str | None = None
  vendor_address: str | None = None
  invoice_number: str | None = None
  invoice_date: date | None = None
  due_date: date | None = None
  subtotal: float | None = None
  tax: float | None = None
  total: float | None = None
  currency: Currency = Field(default=Currency.USD, description="The currency of the invoice")
  line_items: list[LineItem] = []
  raw_text: str | None = None
  confidence_scores: dict[str, float] = {}


class InvoiceResponse(BaseModel):
  """ API response for single invoice """
  id: str
  filename: str
  parsed_data: ParsedInvoice
  created_at: datetime
  updated_at: datetime


class InvoiceListResponse(BaseModel):
  """ Paginated list of invoices """
  invoices: list[InvoiceResponse]
  total: int
  page: int
  per_page: int
  total_pages: int = 1



