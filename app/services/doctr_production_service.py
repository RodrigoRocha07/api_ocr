#!/usr/bin/env python3
"""
Serviço de Produção docTR - OCR otimizado para produção
"""

import time
import logging
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor
    DOCTR_AVAILABLE = True
except ImportError:
    DOCTR_AVAILABLE = False

class DoctrProductionService:
    """Serviço de produção otimizado usando docTR"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.is_initialized = False
        
    def initialize_model(self) -> bool:
        """Inicializa o modelo docTR para produção"""
        if self.is_initialized:
            return True
            
        if not DOCTR_AVAILABLE:
            self.logger.error("❌ docTR não está disponível")
            return False
            
        try:
            self.logger.info("🚀 Inicializando modelo docTR para produção...")
            start_time = time.time()
            
            # Carregar modelo pré-treinado otimizado
            self.model = ocr_predictor(pretrained=True)
            
            init_time = time.time() - start_time
            self.is_initialized = True
            
            self.logger.info(f"✅ Modelo docTR inicializado em {init_time:.2f}s")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar docTR: {e}")
            return False
    
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """Extrai texto usando docTR otimizado para produção"""
        if not self.is_initialized:
            if not self.initialize_model():
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'process_time': 0.0,
                    'word_count': 0,
                    'error': 'Modelo não inicializado'
                }
        
        try:
            start_time = time.time()
            
            # Carregar documento
            doc = DocumentFile.from_images(image_path)
            
            # Processar OCR
            result = self.model(doc)
            
            # Extrair texto e confiança
            text = ""
            confidence = 0
            word_count = 0
            extracted_words = []
            
            for page in result.pages:
                for block in page.blocks:
                    for line in block.lines:
                        line_text = ""
                        line_confidence = 0
                        line_words = 0
                        
                        for word in line.words:
                            line_text += word.value + " "
                            line_confidence += word.confidence
                            line_words += 1
                            extracted_words.append({
                                'text': word.value,
                                'confidence': word.confidence
                            })
                        
                        if line_words > 0:
                            line_confidence = line_confidence / line_words
                            confidence += line_confidence
                            word_count += line_words
                        
                        text += line_text + "\n"
            
            if word_count > 0:
                confidence = confidence / word_count
            
            process_time = time.time() - start_time
            
            return {
                'success': True,
                'text': text.strip(),
                'confidence': confidence,
                'process_time': process_time,
                'word_count': word_count,
                'extracted_words': extracted_words,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro no docTR: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'process_time': 0.0,
                'word_count': 0,
                'error': str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        return {
            'name': 'docTR Production',
            'available': DOCTR_AVAILABLE,
            'initialized': self.is_initialized,
            'description': 'OCR de produção baseado em Deep Learning',
            'framework': 'PyTorch',
            'architecture': 'DBNet + CRNN/Transformer',
            'optimization': 'Production-ready'
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Retorna status de saúde do serviço"""
        return {
            'status': 'healthy' if self.is_initialized else 'unhealthy',
            'model_available': DOCTR_AVAILABLE,
            'model_initialized': self.is_initialized,
            'timestamp': time.time()
        } 