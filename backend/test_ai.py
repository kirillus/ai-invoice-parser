import asyncio

from app.services.ai_parser import parse_invoice_with_ai


async def main():
  sample_text = """
    INVOICE #1234
    From: Acme Corp, 123 Main St, NYC
    Date: 2024-01-15
    Due: 2024-02-15

    Web Development Services   40 hrs x $150   $6,000.00
    Server Hosting              1 mo  x $99     $99.00

    Subtotal: $6,099.00
    Tax (13%): $792.87
    Total: $6,891.87
    """
  result = await parse_invoice_with_ai(sample_text)
  print(result.model_dump_json(indent=2))

if __name__ == "__main__":
  asyncio.run(main())