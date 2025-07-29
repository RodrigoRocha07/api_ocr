from fastapi import FastAPI
from app.api import ocr

app = FastAPI(title="API OCR Tesseract")
 
app.include_router(ocr.router, prefix="/ocr", tags=["OCR"]) 