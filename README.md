## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```


## Project Structure

```
ai-invoice-parser/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # Config
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # AI parsing, OCR
│   │   └── utils/
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/
│       ├── hooks/
│       ├── pages/
│       └── services/
└── docker-compose.yml
```

## License

MIT
