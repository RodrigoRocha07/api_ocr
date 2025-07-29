# 🚀 Deploy na AWS EC2 - API OCR

## 📋 Pré-requisitos

- Conta AWS ativa
- EC2 Instance (recomendado: t3.medium ou superior)
- Security Group configurado
- Chave SSH (.pem)

## 🖥️ Configuração da EC2

### 1. **Criar EC2 Instance**

```bash
# Tipo recomendado
Instance Type: t3.medium (2 vCPU, 4GB RAM)
AMI: Ubuntu 22.04 LTS
Storage: 20GB GP3
Security Group: Portas 22 (SSH), 80 (HTTP), 443 (HTTPS), 8000 (API)
```

### 2. **Security Group**
```
Inbound Rules:
- SSH (22) - Sua IP
- HTTP (80) - 0.0.0.0/0
- HTTPS (443) - 0.0.0.0/0
- Custom TCP (8000) - 0.0.0.0/0 (para API)
```

## 🚀 Deploy Rápido

### **Opção 1: Docker (Recomendado)**

```bash
# Conectar na EC2
ssh -i sua-chave.pem ubuntu@seu-ip-ec2

# Instalar Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# Clonar projeto
git clone https://github.com/seu-usuario/ambiente_ocr.git
cd ambiente_ocr/api_ocr

# Executar com Docker
chmod +x docker-run.sh
./docker-run.sh
```

### **Opção 2: Ambiente Virtual**

```bash
# Conectar na EC2
ssh -i sua-chave.pem ubuntu@seu-ip-ec2

# Instalar dependências
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# Clonar projeto
git clone https://github.com/seu-usuario/ambiente_ocr.git
cd ambiente_ocr

# Criar e ativar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
cd api_ocr
pip install -r requirements.txt

# Executar API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔧 Configuração de Produção

### **1. Usando systemd (Recomendado)**

```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/ocr-api.service
```

```ini
[Unit]
Description=OCR API Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ambiente_ocr/api_ocr
Environment=PATH=/home/ubuntu/ambiente_ocr/venv/bin
ExecStart=/home/ubuntu/ambiente_ocr/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl daemon-reload
sudo systemctl enable ocr-api
sudo systemctl start ocr-api
sudo systemctl status ocr-api
```

### **2. Usando Docker Compose (Produção)**

```bash
# Criar docker-compose.prod.yml
nano docker-compose.prod.yml
```

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: ocr-api-prod
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    restart: unless-stopped
    volumes:
      - ./app:/app/app
    networks:
      - ocr-network

  redis:
    image: redis:7-alpine
    container_name: ocr-redis-prod
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - ocr-network

volumes:
  redis_data:

networks:
  ocr-network:
    driver: bridge
```

```bash
# Executar em produção
docker-compose -f docker-compose.prod.yml up -d
```

## 🌐 Configurar Nginx (Opcional)

```bash
# Instalar Nginx
sudo apt install -y nginx

# Configurar proxy reverso
sudo nano /etc/nginx/sites-available/ocr-api
```

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/ocr-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Configurações de Segurança

### **1. Firewall (UFW)**
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000
```

### **2. SSL/HTTPS (Let's Encrypt)**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

## 📊 Monitoramento

### **1. Logs**
```bash
# Logs da API
sudo journalctl -u ocr-api -f

# Logs do Docker
docker-compose logs -f api
```

### **2. Status do Serviço**
```bash
# Verificar status
sudo systemctl status ocr-api

# Reiniciar se necessário
sudo systemctl restart ocr-api
```

## 🚀 Script de Deploy Automatizado

```bash
#!/bin/bash
# deploy-ec2.sh

echo "🚀 Deployando API OCR na EC2..."

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y docker.io docker-compose git

# Clonar projeto
git clone https://github.com/seu-usuario/ambiente_ocr.git
cd ambiente_ocr/api_ocr

# Executar com Docker
chmod +x docker-run.sh
./docker-run.sh

echo "✅ Deploy concluído!"
echo "🌐 API disponível em: http://seu-ip-ec2:8000"
```

## 📈 Escalabilidade

### **1. Auto Scaling Group**
- Criar Launch Template
- Configurar Auto Scaling Group
- Definir políticas de escala

### **2. Load Balancer**
- Application Load Balancer
- Distribuir tráfego entre instâncias
- Health checks automáticos

## 💰 Estimativa de Custos

### **t3.medium (Recomendado)**
- **CPU:** 2 vCPU
- **RAM:** 4GB
- **Custo:** ~$30/mês
- **Ideal para:** Produção pequena/média

### **t3.large (Para mais tráfego)**
- **CPU:** 2 vCPU
- **RAM:** 8GB
- **Custo:** ~$60/mês
- **Ideal para:** Produção média/grande

## 🎯 Checklist de Deploy

- [ ] EC2 Instance criada
- [ ] Security Group configurado
- [ ] Projeto clonado
- [ ] Dependências instaladas
- [ ] API rodando
- [ ] Firewall configurado
- [ ] Nginx configurado (opcional)
- [ ] SSL configurado (opcional)
- [ ] Monitoramento ativo
- [ ] Backup configurado

## 🆘 Troubleshooting

### **API não inicia**
```bash
# Verificar logs
sudo journalctl -u ocr-api -f

# Verificar dependências
pip list | grep doctr
```

### **Porta 8000 não acessível**
```bash
# Verificar firewall
sudo ufw status

# Verificar se API está rodando
curl http://localhost:8000/ocr/health
```

### **Problemas de memória**
```bash
# Verificar uso de RAM
free -h

# Aumentar swap se necessário
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
``` 