# 🚀 Guia de Instalação - API OCR com docTR

## 📋 Pré-requisitos

- Python 3.9+
- pip
- git

## 🔧 Passo a Passo de Instalação

### 1. Ativar Ambiente Virtual

```bash
# Navegar para o diretório do projeto
cd /Users/rodrigodev/Documents/projetos_python/PROJETOS\ PRINCIPAIS/ambiente_ocr

# Ativar o ambiente virtual
source venv/bin/activate
```

### 2. Verificar Instalação do docTR

```bash
# Verificar se o docTR está instalado
pip list | grep doctr

# Testar importação do docTR
python -c "import doctr; print('✅ docTR instalado com sucesso')"
```

### 3. Instalar docTR (se necessário)

Se o docTR não estiver instalado, execute:

```bash
# Instalar docTR
pip install python-doctr

# Para versão com GPU (se disponível)
# pip install python-doctr[torch]
```

### 4. Verificar Dependências

```bash
# Verificar todas as dependências instaladas
pip list

# Dependências principais que devem estar instaladas:
# - python-doctr
# - torch
# - fastapi
# - uvicorn
# - aiofiles
# - redis (para cache)
```

### 5. Testar Instalação

```bash
# Testar importação completa
python -c "
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
print('✅ docTR funcionando corretamente')
"
```

### 6. Executar a API

```bash
# Navegar para o diretório da API
cd api_ocr

# Executar a API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔍 Solução de Problemas

### Erro: "docTR não está disponível"

**Causa:** Ambiente virtual não ativado ou docTR não instalado

**Solução:**
```bash
# 1. Ativar venv
source venv/bin/activate

# 2. Instalar docTR
pip install python-doctr

# 3. Verificar instalação
python -c "import doctr; print('OK')"
```

### Erro: "Modelo não inicializado"

**Causa:** docTR não consegue carregar o modelo

**Solução:**
```bash
# 1. Verificar conexão com internet (para download do modelo)
# 2. Limpar cache do pip
pip cache purge

# 3. Reinstalar docTR
pip uninstall python-doctr
pip install python-doctr
```

### Erro: "ImportError: No module named 'doctr'"

**Causa:** Ambiente virtual não ativado

**Solução:**
```bash
# Sempre ativar a venv antes de executar
source venv/bin/activate
```

## 📦 Estrutura de Arquivos

```
ambiente_ocr/
├── venv/                    # Ambiente virtual
├── api_ocr/
│   ├── app/
│   │   ├── api/
│   │   │   └── ocr.py      # Endpoints da API
│   │   ├── services/
│   │   │   ├── async_ocr_service.py
│   │   │   └── doctr_production_service.py
│   │   └── main.py         # Aplicação FastAPI
│   └── README_INSTALACAO.md
```

## 🚀 Comandos Rápidos

```bash
# Ativar venv e executar API
source venv/bin/activate && cd api_ocr && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Verificar status
curl http://localhost:8000/ocr/health

# Testar modelo
curl http://localhost:8000/ocr/model/info
```

## 📝 Notas Importantes

1. **Sempre ative a venv** antes de executar qualquer comando
2. O docTR baixa modelos automaticamente na primeira execução
3. A primeira inicialização pode demorar alguns minutos
4. Verifique se há conexão com internet para download dos modelos

## 🆘 Suporte

Se ainda houver problemas:

1. Verifique se a venv está ativada: `which python`
2. Verifique versão do Python: `python --version`
3. Verifique se o docTR está instalado: `pip show python-doctr`
4. Teste importação: `python -c "import doctr"` 