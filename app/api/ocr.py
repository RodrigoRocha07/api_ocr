from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from app.models.ocr import OCRResponse, ServiceStats
from app.services.async_ocr_service import AsyncOCRService
import logging
import asyncio

router = APIRouter()

# Inicializar serviço OCR assíncrono
async_ocr_service = AsyncOCRService()

@router.on_event("startup")
async def startup_event():
    """Inicializa o serviço na startup da aplicação"""
    await async_ocr_service.initialize()

@router.on_event("shutdown")
async def shutdown_event():
    """Limpa recursos na shutdown da aplicação"""
    await async_ocr_service.cleanup()

@router.post("/upload", response_model=OCRResponse)
async def upload_file(file: UploadFile = File(...)):
    """Endpoint principal para OCR assíncrono usando docTR"""
    try:
        # Lê o arquivo de forma assíncrona
        content = await file.read()
        
        # Processa de forma assíncrona
        result = await async_ocr_service.extract_text_async(content, file.filename)
        
        if result.get('success'):
            text = result.get('text', '')
            confidence = result.get('confidence', 0.0)
            quality_score = confidence
            from_cache = result.get('from_cache', False)
            total_time = result.get('total_time', 0.0)
            process_time = result.get('process_time', 0.0)
        else:
            text = ""
            quality_score = 0.0
            from_cache = False
            total_time = result.get('total_time', 0.0)
            process_time = 0.0
            logging.error(f"Erro no OCR assíncrono: {result.get('error')}")
        
        return OCRResponse(
            text=text, 
            quality_score=quality_score,
            from_cache=from_cache,
            total_time=total_time,
            process_time=process_time
        )
        
    except Exception as e:
        logging.error(f"Erro no endpoint /upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Endpoint de health check assíncrono"""
    try:
        import time
        stats = await async_ocr_service.get_service_stats()
        
        return {
            "status": "healthy" if stats['initialized'] else "unhealthy",
            "service": "Async docTR OCR API",
            "stats": stats,
            "timestamp": time.time()
        }
    except Exception as e:
        logging.error(f"Erro no health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

@router.get("/stats", response_model=ServiceStats)
async def get_service_stats():
    """Endpoint para obter estatísticas detalhadas do serviço"""
    try:
        stats = await async_ocr_service.get_service_stats()
        return ServiceStats(**stats)
    except Exception as e:
        logging.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model/info")
async def get_model_info():
    """Endpoint para obter informações sobre o modelo docTR"""
    try:
        model_info = async_ocr_service.doctr_service.get_model_info()
        return {
            "success": True,
            "model_info": model_info
        }
    except Exception as e:
        logging.error(f"Erro ao obter informações do modelo: {e}")
        return {
            "success": False,
            "error": str(e)
        } 