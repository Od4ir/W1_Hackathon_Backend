# 💻 W1_Hackathon_Backend

Este é o repositório para backend para o projeto desenvolvido durante o Hackathon da W1. Responsáveis pelo projeto:

- Anna Beatriz - [LinkedIn]();
- Mariana Tiemi - [LinkedIn]();
- Odair Gonçalves - [LinkedIn]();

O backend será responsável por:

- 🌐 Fornecer APIs REST para comunicação com o Frontend ([Clique para acessar o repositório](#));
- 🧠 Integração com as funcionalidades potencialidas por LLMs ([Clique para acessar o repositório](#));
- 🗃️ Acessar e manipular dados armazenados em um banco PostgreSQL de exemplo;

---

## 📑 Índice
1. [Introdução](#-💻-w1_hackathon_backend)
2. [Índice](#-📑-índice)
3. [Requisitos Técnicos](#-🧱-requisitos-técnicos)
4. [Como rodar o projeto localmente](#-🚀-como-rodar-o-projeto-localmente)
    - [Clonar o repositório](#1-clonar-o-repositório)
    - [Criar e ativar um ambiente virtual](#2-crie-e-ative-um-ambiente-virtual)
    - [Instalação das dependências](#3-instalação-das-dependências)
    - [Rodar o servidor](#4-rodar-o-servidor)
    - [Acessar o servidor](#5-acessar-o-servidor)
5. [Estrutura do projeto](#-📁-estrutura-do-projeto)


## 🧱 Requisitos Técnicos:

Lista de linguagens, bibliotecas e frameworks utilziados:

- **Python 3.10+** - Linguagem de programação;
- **FastAPI** – Framework web leve, rápido e com docs automáticas;
- **Uvicorn** – Servidor ASGI;
- **httpx** – Cliente HTTP async para integração com a LLM;
- **SQLAlchemy** – ORM (integração com PostgreSQL);
- **dotenv** – Variáveis de ambiente;
- **Docker** – Para rodar localmente em container (opcional);

---

## 🚀 Como rodar o projeto localmente

### 1. Clonar o repositório

```bash
git git@github.com:Od4ir/W1_Hackathon_Backend.git
cd W1_Hackathon_Backend
```
### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # no Linux/macOS
venv\Scripts\activate     # no Windows
```

### 3. Instalação das dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar o servidor
```bash
uvicorn app.main:app --reload
```

### 5. Acessar o servidor
- Acesse: http://localhost:8000
- Docs automáticas: http://localhost:8000/docs


## 🚀 Como rodar com Docker

### 1. Construindo a Imagem
```bash
docker build -t w1-backend .
```

### 2. Rodando o container
```bash
docker run -d -p 8000:8000 --env-file .env w1-backend
```
### 3. Acessar o servidor:
- Acesse: http://localhost:8000
- Docs automáticas: http://localhost:8000/docs


## 📁 Estrutura do projeto

```bash
W1_Hackathon_Backend/
├── app/
│   ├── api/           # Rotas da API
│   ├── db/            # Conexão com o banco (PostgreSQL)
│   ├── models/        # Esquemas de dados
│   ├── services/      # Integração com LLM e outras regras
│   └── main.py        # Código principal
├── requirements.txt   # Dependências
├── .env.example       # Variáveis locais
├── Dockerfile         # Documento Docker
└── README.md
```
