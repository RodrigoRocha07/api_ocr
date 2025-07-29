#!/bin/bash

# 🚀 Script de Instalação - API OCR com docTR
# Autor: Rodrigo Dev
# Data: $(date)

echo "🚀 Iniciando instalação da API OCR..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se estamos no diretório correto
if [ ! -d "venv" ]; then
    print_error "Diretório 'venv' não encontrado. Execute este script do diretório raiz do projeto."
    exit 1
fi

print_status "Verificando ambiente virtual..."

# Ativar ambiente virtual
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_success "Ambiente virtual ativado"
else
    print_error "Arquivo de ativação do ambiente virtual não encontrado"
    exit 1
fi

# Verificar Python
print_status "Verificando versão do Python..."
python_version=$(python --version 2>&1)
print_success "Python: $python_version"

# Verificar se requirements.txt existe
if [ -f "api_ocr/requirements.txt" ]; then
    print_status "Instalando dependências do requirements.txt..."
    pip install -r api_ocr/requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Dependências instaladas com sucesso"
    else
        print_error "Falha ao instalar dependências"
        exit 1
    fi
else
    print_warning "requirements.txt não encontrado. Instalando dependências básicas..."
    
    # Instalar dependências básicas
    pip install fastapi uvicorn python-doctr torch torchvision opencv-python redis celery aiofiles
fi

# Verificar se docTR está funcionando
print_status "Verificando instalação do docTR..."
if python -c "import doctr" 2>/dev/null; then
    print_success "docTR importado com sucesso"
else
    print_error "docTR não está funcionando"
    exit 1
fi

# Verificar compatibilidade de versões
print_status "Verificando compatibilidade de versões..."
python -c "
import torch
import doctr
import cv2
import numpy as np
print(f'✅ PyTorch: {torch.__version__}')
print(f'✅ docTR: {doctr.__version__}')
print(f'✅ OpenCV: {cv2.__version__}')
print(f'✅ NumPy: {np.__version__}')
"

# Verificar outras dependências importantes
print_status "Verificando dependências críticas..."
dependencies=("fastapi" "uvicorn" "aiofiles" "redis" "celery" "requests")

for dep in "${dependencies[@]}"; do
    if python -c "import $dep" 2>/dev/null; then
        print_success "$dep: OK"
    else
        print_error "$dep: FALHOU"
        exit 1
    fi
done

# Testar importação completa do docTR
print_status "Testando funcionalidade do docTR..."
if python -c "
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
print('✅ docTR funcionando corretamente')
"; then
    print_success "Teste de funcionalidade do docTR: OK"
else
    print_error "Falha no teste de funcionalidade do docTR"
    exit 1
fi

# Verificar se estamos no diretório da API
if [ ! -f "app/main.py" ]; then
    print_status "Navegando para o diretório da API..."
    cd api_ocr
fi

# Verificar se os arquivos da API existem
if [ ! -f "app/main.py" ]; then
    print_error "Arquivos da API não encontrados"
    exit 1
fi

print_success "✅ Instalação concluída com sucesso!"

echo ""
echo "🚀 Para executar a API:"
echo "   source venv/bin/activate"
echo "   cd api_ocr"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📖 Para mais informações, consulte o README_INSTALACAO.md"
echo ""

# Perguntar se quer executar a API agora
read -p "Deseja executar a API agora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Executando API..."
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi 