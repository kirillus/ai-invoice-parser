const API_BASE = 'http://localhost:8000/api/v1';

export async function uploadInvoice(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/invoices/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }

  return response.json();
}

export async function getInvoices(page = 1) {
  const response = await fetch(`${API_BASE}/invoices?page=${page}`);
  return response.json();
}

export async function getInvoice(id) {
  const response = await fetch(`${API_BASE}/invoices/${id}`);
  return response.json();
}
