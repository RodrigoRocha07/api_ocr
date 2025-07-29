#!/bin/bash

# 🐳 Script para executar API OCR com Docker
# Autor: Rodrigo Dev

echo "🐳 Iniciando API OCR com Docker..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

# Verificar se os arquivos necessários existem
if [ ! -f "Dockerfile" ]; then
    print_error "Dockerfile não encontrado"
    exit 1
fi

if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml não encontrado"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt não encontrado"
    exit 1
fi

print_status "Verificando se containers já estão rodando..."
if docker-compose ps | grep -q "Up"; then
    print_warning "Containers já estão rodando. Parando..."
    docker-compose down
fi

print_status "Construindo imagem Docker..."
docker-compose build --no-cache

if [ $? -ne 0 ]; then
    print_error "Falha na construção da imagem Docker"
    exit 1
fi

print_status "Iniciando serviços..."
docker-compose up -d

if [ $? -ne 0 ]; then
    print_error "Falha ao iniciar serviços"
    exit 1
fi

print_status "Aguardando serviços ficarem prontos..."
sleep 10

# Verificar se a API está respondendo
print_status "Verificando se a API está funcionando..."
for i in {1..30}; do
    if curl -f http://localhost:8000/ocr/health &> /dev/null; then
        print_success "✅ API está funcionando!"
        break
    fi
    
    if [ $i -eq 30 ]; then
        print_error "❌ API não respondeu após 30 tentativas"
        print_status "Verificando logs..."
        docker-compose logs api
        exit 1
    fi
    
    print_status "Tentativa $i/30 - Aguardando..."
    sleep 2
done

print_success "🚀 API OCR iniciada com sucesso!"
echo ""
echo "📋 Informações:"
echo "   🌐 API: http://localhost:8000"
echo "   📖 Docs: http://localhost:8000/docs"
echo "   🔍 Health: http://localhost:8000/ocr/health"
echo "   📊 Stats: http://localhost:8000/ocr/stats"
echo ""
echo "🐳 Comandos úteis:"
echo "   docker-compose logs -f api    # Ver logs da API"
echo "   docker-compose logs -f redis  # Ver logs do Redis"
echo "   docker-compose down           # Parar serviços"
echo "   docker-compose restart api    # Reiniciar API"
echo ""

# Perguntar se quer ver os logs
read -p "Deseja ver os logs da API? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Mostrando logs da API..."
    docker-compose logs -f api
fi 