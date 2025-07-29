# 🐳 Guia Docker - API OCR com docTR

## 📋 Pré-requisitos

- Docker Desktop instalado
- Docker Compose instalado
- Pelo menos 4GB de RAM disponível
- Conexão com internet (para download das imagens)

## 🚀 Execução Rápida

### Método 1: Script Automatizado (Recomendado)

```bash
# Navegar para o diretório da API
cd api_ocr

# Tornar o script executável
chmod +x docker-run.sh

# Executar
./docker-run.sh
```

### Método 2: Comandos Manuais

```bash
# Construir e iniciar
docker-compose up --build -d

# Ver logs
docker-compose logs -f api

# Parar serviços
docker-compose down
```

## 📦 Estrutura Docker

```
api_ocr/
├── Dockerfile              # Imagem da API
├── docker-compose.yml      # Orquestração dos serviços
├── docker-run.sh          # Script de execução
├── requirements.txt       # Dependências Python
└── app/                  # Código da aplicação
```

## 🔧 Serviços

### 1. API OCR (`api`)
- **Porta:** 8000
- **Imagem:** Python 3.9 + docTR
- **Health Check:** `/ocr/health`
- **Volumes:** 
  - `./app:/app/app` (código)
  - `doctr_cache:/app/.doctr_cache` (cache dos modelos)

### 2. Redis Cache (`redis`)
- **Porta:** 6379
- **Imagem:** Redis 7 Alpine
- **Persistência:** Volume `redis_data`
- **Configuração:** Cache com limite de 256MB

## 🛠️ Comandos Úteis

### Gerenciamento de Containers

```bash
# Ver status dos containers
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f api
docker-compose logs -f redis

# Reiniciar apenas a API
docker-compose restart api

# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

### Debugging

```bash
# Entrar no container da API
docker-compose exec api bash

# Ver logs detalhados
docker-compose logs --tail=100 api

# Verificar recursos
docker stats
```

### Limpeza

```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Limpeza completa
docker system prune -a
```

## 🔍 Troubleshooting

### Erro: "Port already in use"

```bash
# Verificar o que está usando a porta 8000
lsof -i :8000

# Parar processo ou usar porta diferente
docker-compose up -d --scale api=0
```

### Erro: "Out of memory"

```bash
# Aumentar memória do Docker Desktop
# Ou reduzir recursos no docker-compose.yml
```

### Erro: "Model not initialized"

```bash
# Verificar logs da API
docker-compose logs api

# Reiniciar apenas a API
docker-compose restart api

# Verificar se o cache está funcionando
docker-compose exec redis redis-cli ping
```

### Erro: "Build failed"

```bash
# Limpar cache do Docker
docker builder prune

# Reconstruir sem cache
docker-compose build --no-cache

# Verificar requirements.txt
cat requirements.txt
```

## 📊 Monitoramento

### Health Checks

```bash
# Verificar saúde da API
curl http://localhost:8000/ocr/health

# Verificar saúde do Redis
docker-compose exec redis redis-cli ping
```

### Métricas

```bash
# Ver estatísticas da API
curl http://localhost:8000/ocr/stats

# Ver informações do modelo
curl http://localhost:8000/ocr/model/info
```

## 🔒 Segurança

- ✅ Usuário não-root no container
- ✅ Health checks configurados
- ✅ Volumes isolados
- ✅ Rede dedicada
- ✅ Limite de memória no Redis

## 📈 Performance

### Otimizações Implementadas

- **Multi-stage build** para reduzir tamanho da imagem
- **Cache de dependências** para builds mais rápidos
- **Volume persistente** para cache do docTR
- **Health checks** para monitoramento
- **Limite de memória** no Redis

### Recomendações

- **RAM mínima:** 4GB
- **CPU:** 2 cores
- **Disco:** 10GB livres
- **Rede:** Conexão estável para download dos modelos

## 🚀 Deploy em Produção

### Variáveis de Ambiente

```bash
# Criar arquivo .env
REDIS_URL=redis://redis:6379
DOCTR_CACHE_DIR=/app/.doctr_cache
PYTHONUNBUFFERED=1
```

### Comandos de Deploy

```bash
# Build para produção
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Backup dos dados
docker-compose exec redis redis-cli BGSAVE
```

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `docker-compose logs api`
2. Verifique o status: `docker-compose ps`
3. Teste a conectividade: `curl http://localhost:8000/ocr/health`
4. Consulte este README para troubleshooting 