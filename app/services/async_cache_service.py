import json
import hashlib
import logging
import os
from typing import Optional, Any, Dict
import asyncio
from datetime import timedelta

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class AsyncCacheService:
    """Serviço de cache assíncrono para otimizar performance"""
    
    def __init__(self, redis_url: str = None):
        self.logger = logging.getLogger(__name__)
        # Usar variável de ambiente ou padrão
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_client = None
        self.is_connected = False
        
    async def connect(self) -> bool:
        """Conecta ao Redis"""
        if not REDIS_AVAILABLE:
            self.logger.warning("⚠️ Redis não disponível - cache desabilitado")
            return False
            
        try:
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            self.is_connected = True
            self.logger.info("✅ Cache Redis conectado")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao conectar Redis: {e}")
            return False
    
    async def disconnect(self):
        """Desconecta do Redis"""
        if self.redis_client:
            await self.redis_client.close()
            self.is_connected = False
    
    def _generate_key(self, content: bytes, prefix: str = "ocr") -> str:
        """Gera chave única baseada no conteúdo"""
        content_hash = hashlib.md5(content).hexdigest()
        return f"{prefix}:{content_hash}"
    
    async def get_cached_result(self, content: bytes) -> Optional[Dict[str, Any]]:
        """Busca resultado em cache"""
        if not self.is_connected:
            return None
            
        try:
            key = self._generate_key(content)
            cached_data = await self.redis_client.get(key)
            if cached_data:
                result = json.loads(cached_data)
                self.logger.info(f"🎯 Cache hit para {key}")
                return result
            return None
        except Exception as e:
            self.logger.error(f"❌ Erro ao buscar cache: {e}")
            return None
    
    async def set_cached_result(self, content: bytes, result: Dict[str, Any], 
                              ttl: int = 3600) -> bool:
        """Salva resultado no cache"""
        if not self.is_connected:
            return False
            
        try:
            key = self._generate_key(content)
            await self.redis_client.setex(
                key, 
                ttl, 
                json.dumps(result, ensure_ascii=False)
            )
            self.logger.info(f"💾 Cache salvo para {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar cache: {e}")
            return False
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        if not self.is_connected:
            return {"connected": False, "keys": 0, "memory": 0}
            
        try:
            info = await self.redis_client.info()
            keys = await self.redis_client.dbsize()
            return {
                "connected": True,
                "keys": keys,
                "memory": info.get("used_memory_human", "0B"),
                "uptime": info.get("uptime_in_seconds", 0)
            }
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter stats: {e}")
            return {"connected": False, "error": str(e)} 