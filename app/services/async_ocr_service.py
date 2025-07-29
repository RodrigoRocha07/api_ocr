import asyncio
import time
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import aiofiles
import tempfile
import os

from app.services.doctr_production_service import DoctrProductionService
from app.services.async_cache_service import AsyncCacheService

class AsyncOCRService:
    """Serviço OCR totalmente assíncrono com cache e processamento otimizado"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.doctr_service = DoctrProductionService()
        self.cache_service = AsyncCacheService()
        self.processing_semaphore = asyncio.Semaphore(3)  # Máximo 3 processamentos simultâneos
        self.is_initialized = False
        
    async def initialize(self) -> bool:
        """Inicializa o serviço assíncrono"""
        if self.is_initialized:
            return True
            
        try:
            # Inicializa docTR
            if not self.doctr_service.initialize_model():
                return False
                
            # Conecta cache
            await self.cache_service.connect()
            
            self.is_initialized = True
            self.logger.info("✅ Serviço OCR assíncrono inicializado")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar serviço assíncrono: {e}")
            return False
    
    async def extract_text_async(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Extrai texto de forma assíncrona com cache"""
        start_time = time.time()
        
        try:
            # Verifica cache primeiro
            cached_result = await self.cache_service.get_cached_result(file_content)
            if cached_result:
                cached_result['from_cache'] = True
                cached_result['total_time'] = time.time() - start_time
                return cached_result
            
            # Processa com semáforo para limitar concorrência
            async with self.processing_semaphore:
                result = await self._process_image_async(file_content, filename)
                
                # Salva no cache
                if result.get('success'):
                    await self.cache_service.set_cached_result(file_content, result)
                
                result['from_cache'] = False
                result['total_time'] = time.time() - start_time
                return result
                
        except Exception as e:
            self.logger.error(f"❌ Erro no processamento assíncrono: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'process_time': 0.0,
                'error': str(e),
                'from_cache': False,
                'total_time': time.time() - start_time
            }
    
    async def _process_image_async(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Processa imagem de forma assíncrona"""
        try:
            # Salva arquivo temporário
            suffix = Path(filename).suffix
            async with aiofiles.tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=suffix
            ) as temp_file:
                await temp_file.write(file_content)
                temp_path = temp_file.name
            
            try:
                # Processa com docTR (síncrono, mas em thread separada)
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, 
                    self.doctr_service.extract_text, 
                    temp_path
                )
                return result
            finally:
                # Limpa arquivo temporário
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            self.logger.error(f"❌ Erro no processamento de imagem: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'process_time': 0.0,
                'error': str(e)
            }
    
    async def get_service_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do serviço"""
        cache_stats = await self.cache_service.get_cache_stats()
        
        return {
            'service': 'Async OCR Service',
            'initialized': self.is_initialized,
            'doctr_available': self.doctr_service.is_initialized,
            'cache': cache_stats,
            'semaphore': {
                'max_concurrent': self.processing_semaphore._value,
                'available': self.processing_semaphore._value
            }
        }
    
    async def cleanup(self):
        """Limpa recursos"""
        await self.cache_service.disconnect() 