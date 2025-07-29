# 🗄️ GUIA COMPLETO - REDIS PARA API OCR

## 📋 **O QUE É O REDIS?**

O **Redis** é um banco de dados **in-memory** (em memória) super rápido que estamos usando como **cache** para a API OCR.

### **🎯 Por que usar Redis?**
- **⚡ Velocidade**: Acesso em ~0.001s vs 2.4s de processamento
- **💰 Economia**: Reduz carga no servidor
- **🔄 Reutilização**: Mesmo documento = resultado instantâneo
- **📊 Monitoramento**: Estatísticas em tempo real

## 🚀 **INSTALAÇÃO E CONFIGURAÇÃO**

### **1. Instalar Redis (macOS):**
```bash
# Instalar via Homebrew
brew install redis

# Iniciar como serviço
brew services start redis

# Verificar se está rodando
redis-cli ping
# Resposta: PONG
```

### **2. Instalar Redis (Ubuntu/Debian):**
```bash
# Instalar
sudo apt update
sudo apt install redis-server

# Iniciar serviço
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verificar status
sudo systemctl status redis-server
```

### **3. Instalar Redis (Windows):**
```bash
# Via WSL2 (recomendado)
# Ou baixar de: https://redis.io/download
```

## 🔧 **COMANDOS BÁSICOS DO REDIS**

### **Conectar ao Redis:**
```bash
redis-cli
```

### **Comandos úteis:**
```bash
# Ver todas as chaves
KEYS *

# Ver chaves específicas
KEYS ocr:*

# Ver valor de uma chave
GET ocr:abc123

# Ver TTL (tempo de vida)
TTL ocr:abc123

# Deletar chave
DEL ocr:abc123

# Limpar tudo
FLUSHALL

# Estatísticas
INFO

# Sair
EXIT
```

## 🏗️ **COMO FUNCIONA NA API OCR**

### **1. Fluxo de Cache:**
```
📤 Upload Documento
    ↓
🔍 Verificar Cache (Redis)
    ↓
✅ Cache HIT? → Retornar resultado (0.001s)
❌ Cache MISS? → Processar com docTR (2.4s)
    ↓
💾 Salvar no Cache
    ↓
📤 Retornar resultado
```

### **2. Geração de Chaves:**
```python
# Cada documento gera uma chave única
import hashlib

def gerar_chave(content):
    return f"ocr:{hashlib.md5(content).hexdigest()}"

# Exemplo:
# Documento: cnh.sena.jpeg
# Chave: ocr:ff8520de61da2286f4422ebe46f38f9b
```

### **3. Estrutura do Cache:**
```json
{
  "ocr:ff8520de61da2286f4422ebe46f38f9b": {
    "text": "REPUBLICA FEDERATIVA DO BRASIL...",
    "confidence": 0.85,
    "process_time": 2.4,
    "word_count": 15,
    "timestamp": 1640995200
  }
}
```

## 📊 **MONITORAMENTO E ESTATÍSTICAS**

### **1. Via API:**
```bash
# Ver estatísticas do cache
curl -X GET "http://localhost:8000/ocr/stats"

# Resposta:
{
  "service": "Async OCR Service",
  "cache": {
    "connected": true,
    "keys": 5,
    "memory": "2.1M",
    "uptime": 3600
  }
}
```

### **2. Via Redis CLI:**
```bash
# Conectar
redis-cli

# Ver estatísticas
INFO

# Ver chaves OCR
KEYS ocr:*

# Ver memória usada
INFO memory
```

## ⚙️ **CONFIGURAÇÕES AVANÇADAS**

### **1. Configurar TTL (Tempo de Vida):**
```python
# No código da API
await cache_service.set_cached_result(
    content, 
    result, 
    ttl=3600  # 1 hora (em segundos)
)
```

### **2. Configurar Redis URL:**
```python
# Padrão
redis_url = "redis://localhost:6379"

# Com senha
redis_url = "redis://:senha@localhost:6379"

# Com banco específico
redis_url = "redis://localhost:6379/1"
```

### **3. Configurar Pool de Conexões:**
```python
# Para alta concorrência
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=20
)
```

## 🚨 **TROUBLESHOOTING**

### **1. Redis não conecta:**
```bash
# Verificar se está rodando
brew services list | grep redis

# Reiniciar
brew services restart redis

# Verificar porta
lsof -i :6379
```

### **2. Erro de conexão na API:**
```python
# Logs mostram:
ERROR:app.services.async_cache_service:❌ Erro ao conectar Redis

# Solução: Verificar se Redis está rodando
redis-cli ping
```

### **3. Cache não funciona:**
```bash
# Verificar chaves
redis-cli KEYS ocr:*

# Verificar TTL
redis-cli TTL ocr:chave_exemplo

# Limpar cache se necessário
redis-cli FLUSHALL
```

## 📈 **BENEFÍCIOS DE PERFORMANCE**

### **Comparação de Velocidade:**
| Cenário | Tempo | Melhoria |
|---------|-------|----------|
| **Primeira vez** | 2.4s | - |
| **Cache HIT** | 0.001s | **2400x mais rápido** |
| **Múltiplas requisições** | 0.001s cada | **Escalável** |

### **Economia de Recursos:**
- **CPU**: 95% menos processamento
- **Memória**: Reutilização de resultados
- **Rede**: Menos tráfego
- **Tempo**: Resposta instantânea

## 🎯 **CASOS DE USO**

### **1. Documentos Repetidos:**
```bash
# Usuário envia mesmo documento várias vezes
# Primeira vez: 2.4s
# Segunda vez: 0.001s ✅
```

### **2. Alta Concorrência:**
```bash
# 100 usuários enviam mesmo documento
# Sem cache: 100 × 2.4s = 240s
# Com cache: 1 × 2.4s + 99 × 0.001s = 2.5s ✅
```

### **3. Backup e Restore:**
```bash
# Backup do cache
redis-cli BGSAVE

# Restore do cache
redis-cli --pipe < backup.rdb
```

## 🔒 **SEGURANÇA**

### **1. Configurar Senha:**
```bash
# Editar /opt/homebrew/etc/redis.conf
requirepass sua_senha_aqui

# Reiniciar
brew services restart redis
```

### **2. Limitar Conexões:**
```bash
# No redis.conf
maxclients 100
```

### **3. Backup Automático:**
```bash
# Configurar backup
save 900 1
save 300 10
save 60 10000
```

## 🎉 **CONCLUSÃO**

O Redis transforma a API OCR de:
- **Lenta** (2.4s) → **Instantânea** (0.001s)
- **Cara** (CPU intensivo) → **Eficiente** (cache)
- **Limitada** (1 por vez) → **Escalável** (múltiplas)

**Resultado: API 2400x mais rápida para documentos repetidos!** 🚀 