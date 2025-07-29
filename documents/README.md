# API OCR Tesseract com Machine Learning

API para leitura de documentos via OCR utilizando Tesseract e pós-processamento com Machine Learning, desenvolvida com FastAPI.

## Objetivo
Receber documentos via upload e retornar o texto extraído com alta fidelidade usando técnicas avançadas de pré-processamento e ML.

## Funcionalidades

### 🔧 **Pré-processamento Avançado**
- Redimensionamento inteligente
- Filtro bilateral para redução de ruído
- Equalização de histograma (CLAHE)
- Binarização adaptativa
- Morfologia para limpeza

### 🤖 **Pós-processamento com Machine Learning**
- Correção ortográfica com SymSpell
- Correção de contexto com BERT (português)
- Score de qualidade do texto extraído
- Limpeza inteligente de caracteres

### 📊 **Endpoints Disponíveis**

#### 1. `/ocr/upload` (Recomendado)
- Processamento completo com ML
- Melhor qualidade de texto
- Score de qualidade incluído

#### 2. `/ocr/upload-basic`
- Processamento sem ML
- Mais rápido
- Indicado para documentos simples

#### 3. `/ocr/upload-advanced`
- Configurações customizáveis
- Parâmetros: `use_ml`, `psm`
- Controle total do processamento

## Como rodar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Certifique-se de que o Tesseract está instalado:
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   ```

3. Execute a API:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Acesse a documentação:
   ```
   http://localhost:8000/docs
   ```

## Exemplo de Uso

```python
import requests

# Upload de documento com ML
files = {'file': open('documento.jpg', 'rb')}
response = requests.post('http://localhost:8000/ocr/upload', files=files)
result = response.json()

print(f"Texto: {result['text']}")
print(f"Qualidade: {result['quality_score']:.3f}")
```

## Estrutura do Projeto

- `app/api/` - Rotas da API
- `app/core/` - Configurações e utilitários
- `app/services/` - Lógica de negócio (OCR + ML)
- `app/models/` - Modelos Pydantic
- `tests/` - Testes automatizados

## Tecnologias Utilizadas

- **FastAPI** - Framework web assíncrono
- **Tesseract** - OCR engine
- **OpenCV** - Processamento de imagem
- **Transformers** - Modelos de linguagem (BERT)
- **SymSpell** - Correção ortográfica
- **Pillow** - Manipulação de imagens

## Performance

- **Processamento básico**: ~1-2 segundos
- **Processamento com ML**: ~3-5 segundos
- **Melhoria de qualidade**: 15-40% (dependendo do documento) 