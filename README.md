# 🚀 API OCR com docTR

API de OCR assíncrona usando docTR, FastAPI e Redis para cache.

## 📁 Documentação

Toda a documentação está organizada na pasta `documents/`:

### 📋 Guias de Instalação
- [`documents/README_INSTALACAO.md`](documents/README_INSTALACAO.md) - Guia completo de instalação
- [`documents/README.md`](documents/README.md) - Documentação original do projeto

### 🐳 Docker
- [`documents/README_DOCKER.md`](documents/README_DOCKER.md) - Guia para execução com Docker

### 🏗️ Arquitetura
- [`documents/ESTRUTURA_FINAL.md`](documents/ESTRUTURA_FINAL.md) - Estrutura do projeto
- [`documents/GUIA_REDIS.md`](documents/GUIA_REDIS.md) - Como o Redis funciona no projeto

### 🚀 Deploy
- [`documents/DEPLOY_GUIDE.md`](documents/DEPLOY_GUIDE.md) - Guia de deploy em produção
- [`documents/AWS_DEPLOY_GUIDE.md`](documents/AWS_DEPLOY_GUIDE.md) - Deploy específico na AWS EC2

## ⚡ Execução Rápida

### Método 1: Script Automatizado
```bash
chmod +x install.sh
./install.sh
```

### Método 2: Docker
```bash
chmod +x docker-run.sh
./docker-run.sh
```

### Método 3: Manual
```bash
source ../venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Endpoints

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/ocr/health

## 📚 Mais Informações

Consulte a pasta `documents/` para informações detalhadas sobre:
- Instalação e configuração
- Arquitetura do sistema
- Como usar Docker
- Deploy em produção
- Funcionamento do Redis 