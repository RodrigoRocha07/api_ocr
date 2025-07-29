# ☁️ GUIA DE DEPLOY - API OCR NA NUVEM

## 🚀 **OPÇÕES DE DEPLOY**

### **1. 🐳 DOCKER COMPOSE (MAIS FÁCIL)**

#### **Local/VM:**
```bash
# Subir tudo
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Parar
docker-compose down
```

#### **VPS/Cloud:**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Clonar projeto
git clone seu-repositorio
cd api_ocr_tesseract

# Subir
docker-compose up -d
```

### **2. 🌊 KUBERNETES (ESCALÁVEL)**

#### **Deploy no GKE/AKS/EKS:**
```bash
# Criar cluster
gcloud container clusters create ocr-cluster

# Aplicar deployments
kubectl apply -f k8s/
```

### **3. ☁️ SERVIÇOS GERENCIADOS**

#### **Heroku:**
```bash
# Criar app
heroku create sua-api-ocr

# Configurar Redis
heroku addons:create heroku-redis:hobby-dev

# Deploy
git push heroku main
```

#### **Railway:**
```bash
# Conectar repositório
railway login
railway init

# Deploy automático
git push origin main
```

## 🗄️ **OPÇÕES DE REDIS**

### **1. 🆓 REDIS CLOUD (GRATUITO)**
```bash
# 1. Criar conta em: https://redis.com/try-free/
# 2. Criar database
# 3. Copiar URL de conexão
REDIS_URL=redis://username:password@host:port
```

### **2. 🐳 REDIS EM CONTAINER**
```yaml
# Já configurado no docker-compose.yml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

### **3. ☁️ REDIS GERENCIADO**
- **AWS ElastiCache**: $15/mês
- **Google Memorystore**: $20/mês
- **Azure Cache**: $20/mês

## 🔧 **CONFIGURAÇÃO DE PRODUÇÃO**

### **1. Variáveis de Ambiente:**
```bash
# .env
REDIS_URL=redis://seu-redis:6379
PYTHONPATH=/app
LOG_LEVEL=INFO
```

### **2. Configurar Nginx (Opcional):**
```nginx
# /etc/nginx/sites-available/ocr-api
server {
    listen 80;
    server_name sua-api.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **3. SSL com Let's Encrypt:**
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Gerar certificado
sudo certbot --nginx -d sua-api.com
```

## 📊 **MONITORAMENTO**

### **1. Health Checks:**
```bash
# Verificar API
curl http://sua-api.com/ocr/health

# Verificar Redis
curl http://sua-api.com/ocr/stats
```

### **2. Logs:**
```bash
# Docker
docker-compose logs -f api

# Kubernetes
kubectl logs -f deployment/ocr-api
```

### **3. Métricas:**
```bash
# Estatísticas da API
curl http://sua-api.com/ocr/stats

# Estatísticas do Redis
redis-cli -h seu-redis INFO
```

## 🚀 **DEPLOY RÁPIDO**

### **Opção 1: Docker Compose (Recomendado)**
```bash
# 1. Clonar projeto
git clone https://github.com/seu-usuario/api_ocr_tesseract.git
cd api_ocr_tesseract

# 2. Subir com Docker
docker-compose up -d

# 3. Testar
curl http://localhost:8000/ocr/health
```

### **Opção 2: Sem Redis (Fallback)**
```bash
# A API funciona sem Redis, só fica mais lenta
# Remover Redis do docker-compose.yml e subir só a API
docker-compose up api
```

### **Opção 3: Redis Cloud**
```bash
# 1. Criar conta no Redis Cloud
# 2. Configurar REDIS_URL
export REDIS_URL=redis://username:password@host:port

# 3. Subir API
docker-compose up api
```

## 💰 **CUSTOS ESTIMADOS**

### **Opção Gratuita:**
- **VPS**: $5/mês (DigitalOcean, Linode)
- **Redis**: Gratuito (Redis Cloud 30MB)
- **Total**: ~$5/mês

### **Opção Profissional:**
- **VPS**: $20/mês (2GB RAM)
- **Redis**: $5/mês (Redis Cloud)
- **Total**: ~$25/mês

### **Opção Escalável:**
- **Kubernetes**: $50/mês
- **Redis**: $15/mês (AWS ElastiCache)
- **Total**: ~$65/mês

## 🔒 **SEGURANÇA**

### **1. Firewall:**
```bash
# Permitir apenas portas necessárias
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### **2. Redis com Senha:**
```bash
# Configurar senha no Redis
redis-cli CONFIG SET requirepass "sua_senha_forte"

# Usar na API
REDIS_URL=redis://:sua_senha_forte@localhost:6379
```

### **3. Rate Limiting:**
```nginx
# Limitar requisições
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

## 🎯 **CHECKLIST DE DEPLOY**

- [ ] **Código testado** localmente
- [ ] **Docker** configurado
- [ ] **Redis** configurado
- [ ] **Variáveis de ambiente** definidas
- [ ] **Health checks** funcionando
- [ ] **SSL** configurado (opcional)
- [ ] **Monitoramento** ativo
- [ ] **Backup** configurado
- [ ] **Documentação** atualizada

## 🎉 **RESULTADO**

Após o deploy, sua API estará disponível em:
- **URL**: `https://sua-api.com`
- **Health**: `https://sua-api.com/ocr/health`
- **Docs**: `https://sua-api.com/docs`

**Pronto para processar milhões de documentos com performance máxima!** 🚀 