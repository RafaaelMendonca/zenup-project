# 🧠 ZenUp Project — Chatbot Emocional com FastAPI + Redis + Groq

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Groq API](https://img.shields.io/badge/Groq-LLM-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📑 Índice

1. Visão Geral  
2. Arquitetura do Projeto  
3. Instalação e Configuração  
4. Endpoints da API  
5. Segurança e Boas Práticas  
6. Fluxo de Funcionamento  
7. Execução Local  
8. Tecnologias Utilizadas  
9. Autor  
10. Licença  

---

## 🚀 Visão Geral

O **ZenUp Project** é um chatbot de **apoio emocional seguro**, construído em **Python (FastAPI)** e integrado ao **Redis** para armazenar o histórico de conversas.  
Ele se conecta ao **Groq API** (modelo *Llama 3.3-70b-versatile*) para gerar respostas empáticas e coerentes, com foco em **segurança emocional**, **contexto persistente** e **tratamento responsável de crises**.

---

## 🧩 Arquitetura do Projeto

zenup-project/  
├── chatbot/  
│   └── chatbot.py                # Núcleo lógico e integração com Groq API  
├── controllers/  
│   └── chatbot_controller.py     # Rotas e autenticação  
├── model/  
│   └── redis_model.py            # Gerenciamento do histórico via Redis  
├── main.py                       # Inicialização da API FastAPI  
├── requirements.txt              # Dependências do projeto  
├── .env                          # Variáveis de ambiente  
└── venv/                         # Ambiente virtual local  

---

## ⚙️️ Instalação e Configuração

### 1️⃣ Clone o repositório  
git clone https://github.com/RafaaelMendonca/zenup-project.git  
cd zenup-project  

### 2️⃣ Crie e ative o ambiente virtual  
python -m venv venv  

**Linux / Mac**  
source venv/bin/activate  

**Windows**  
venv\Scripts\activate  

### 3️⃣ Instale as dependências  
pip install -r requirements.txt  

### 4️⃣ Configure o arquivo `.env`  
Crie o arquivo `.env` na raiz do projeto e adicione:  

API_SECRET_KEY=sua_chave_secreta  
GROQ_API_KEY=sua_chave_groq  
REDIS_HOST=localhost  
REDIS_PORT=6379  

---

## 💬 Endpoints da API

### 🔐 1. Login  
Gera o token de acesso para autenticação nos demais endpoints.  

**Endpoint:**  
POST /login  

**Body:**  
{  
  "chave": "sua_chave_de_api"  
}  

**Resposta:**  
{  
  "token": **token_gerado**
}  

---

### 🧠 2. Chat  
Recebe uma mensagem do usuário e retorna a resposta gerada pelo modelo LLM da Groq.  

**Endpoint:**  
POST /chat  

**Headers:**  
Authorization: Bearer **TOKEN**
Content-Type: application/json  

**Body:**  
{  
    "id": 123,  
    "texto": "estou me sentindo muito triste"  
}  

**Resposta:**  
{  
    "mensagem": "Sinto muito que você esteja passando por isso. Estou aqui para ouvir e apoiar você."  
}  

✅ Forma correta de chamar o `/chat`:  

Corpo da requisição:  
{  
  "id": 123,  
  "texto": "estou me sentindo muito triste"  
}  

Cabeçalho (headers):  
Authorization: Bearer **TOKEN**
Content-Type: application/json  

---

### 🧾 3. Gerar Resumo  
Gera um resumo do histórico de conversa armazenado no Redis.  

**Endpoint:**  
GET /resumo/{id_usuario}  

**Headers:**  
Authorization: Bearer **TOKEN** 

**Resposta:**  
{  
    "resumo": "O usuário expressou sentimentos de tristeza e busca apoio emocional."  
}  

---

### 🤖 4. Mensagem Proativa  
Gera uma mensagem automática de apoio emocional ao usuário.  

**Endpoint:**  
GET /ia_proativa/{id_usuario}  

**Resposta:**  
{  
    "mensagem": "Olá! Notei que você está passando por momentos difíceis. Estou aqui para ouvir e fornecer apoio emocional."  
}  

---

## 🛡️ Segurança e Boas Práticas

| Mecanismo | Descrição |  
|------------|------------|  
| Autenticação | Via token gerado no `/login` com base na `API_SECRET_KEY`. |  
| Sanitização | Todo texto é filtrado antes de ser enviado ao modelo. |  
| Detecção de Crise | Regex detecta frases de autoagressão ou risco. |  
| Limite de Mensagens | Cada mensagem é truncada para 4000 caracteres. |  
| Proteção contra Prompt Injection | Remove tokens como `role: system` e `instruções:`. |  
| Conexão Segura com Redis | Operações envoltas em try/except com logs de erro. |  

---

## 🧱 Fluxo de Funcionamento

Fluxo simplificado de execução:

Usuário → API `/login` → Retorna token  
Usuário → API `/chat` → Armazena mensagem no Redis  
API → Groq (modelo Llama 3.3) → Gera resposta  
Resposta → Redis → Usuário  

---

## 🧰 Tecnologias Utilizadas

| Tecnologia | Função |  
|-------------|--------|  
| Python 3.10+ | Linguagem principal |  
| FastAPI | Framework de API assíncrona |  
| Redis | Armazenamento de contexto e cache |  
| Groq API | LLM (Llama 3.3) para geração de respostas |  
| dotenv | Gerenciamento de variáveis de ambiente |  
| Pydantic | Validação e tipagem dos dados |  
| Logging | Registro de erros e auditoria |  
| Secrets | Geração de tokens seguros |  

---

## 🧠 Execução Local

Para executar o servidor localmente:  

uvicorn main:app --reload  

Acesse:  
http://127.0.0.1:8000/docs  

---

## 👨‍💻 Autor

**Rafael Mendonça**  
📧 contato.rafael2023@gmail.com
💼 [LinkedIn](https://www.linkedin.com/in/rafaaelmendonca/)  
🐙 [GitHub](https://github.com/RafaaelMendonca)  

---

## 🏷️ Licença

Este projeto é distribuído sob a licença de **Nozes (o povo estudante hehe)**.  
Sinta-se à vontade para usar, modificar e contribuir. 💙  

---

> “A tecnologia pode ouvir, mas é o humano que acolhe.”
