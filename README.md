# 🖼 ImageAI Pro

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/Licença-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

> **Processamento inteligente de imagens com IA — direto do terminal.**

---

## 📌 Sobre o Projeto

O **ImageAI Pro** é uma ferramenta CLI interativa desenvolvida pela **Evolucy Digital** para processamento em lote de imagens com o apoio de inteligência artificial. Através de um terminal com interface profissional e rica em cores, o usuário pode remover marcas d'água de imagens utilizando o modelo de deep learning **LaMa** (via IOPaint), e renomear imagens automaticamente com nomes criativos ou descritivos gerados pelo **GPT-4o Vision** via OpenRouter.

---

## ✨ Funcionalidades

- 🧹 **Remoção de Marca D'água** — Detecta e apaga marcas d'água de imagens em lote usando o modelo LaMa via IOPaint. Permite escolher o canto de posição da marca ou inserir coordenadas customizadas em percentual.

- ✏️ **Renomeação com IA** — Analisa cada imagem com GPT-4o Vision via OpenRouter e sugere um nome automaticamente em dois estilos:
  - 🎨 **Criativo** — Curto, marketeiro e impactante. Ex: `Vida_Maritima.jpg`
  - 📋 **Descritivo** — Técnico e detalhado. Ex: `Tabua_Resina_Marmoreizada_Efeito_Agua_Premium.jpg`

---

## 📁 Estrutura de Pastas

```
ImageAI Pro/
├── main.py               # Entry point com menu interativo
├── config.py             # Configurações e variáveis de ambiente
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis secretas (não versionado)
├── .env.example          # Modelo do arquivo .env
├── .gitignore
└── utils/
    ├── inpainter.py      # Pipeline de remoção de marca d'água (LaMa)
    └── renamer.py        # Integração com OpenRouter (GPT-4o Vision)
```

---

## ⚙️ Pré-requisitos

- Python **3.11+**
- `pip` instalado
- Conta no [OpenRouter](https://openrouter.ai) com uma API Key ativa (necessária apenas para o módulo de renomeação)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/imageai-pro.git
cd imageai-pro
```

### 2. Crie e ative o ambiente virtual com Python 3.11

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com sua API Key:

```bash
copy .env.example .env
```

Abra o `.env` e insira sua chave:

```env
OPENROUTER_API_KEY=sua_chave_aqui
```

---

## ▶️ Como Usar

Com o ambiente virtual ativo, execute:

```bash
py -3.11 main.py
```

O programa exibe um **menu interativo no terminal** com as opções:

```
[1]  🧹  Remover Marca D'água
[2]  ✏  Renomear Imagens com IA
[0]  🚪  Sair
```

Basta escolher a operação desejada e seguir as instruções que aparecem na tela. Ao final de cada operação, um resumo detalhado é exibido em tabela.

> 💡 Use `CTRL + C` a qualquer momento para cancelar a operação atual e voltar ao menu principal.

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Chave da API do OpenRouter (obrigatória para renomeação com IA)
OPENROUTER_API_KEY=sua_chave_aqui

# URL da API (valor padrão já definido no config.py)
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions

# Modelo de visão a ser utilizado
MODELO_VISAO=openai/gpt-4o
```

> ⚠️ O arquivo `.env` está listado no `.gitignore` e **nunca será enviado ao GitHub.**

---

## 🛠 Tecnologias Utilizadas

| Tecnologia        | Função                                  |
| ----------------- | --------------------------------------- |
| 🐍 Python 3.11    | Linguagem base do projeto               |
| 🎨 IOPaint (LaMa) | Motor de remoção de marca d'água        |
| 🤖 OpenRouter API | Gateway para acesso ao GPT-4o Vision    |
| 📷 OpenCV         | Manipulação e leitura de imagens        |
| 💻 Rich           | Interface visual no terminal            |
| 🔤 PyFiglet       | Banner ASCII no cabeçalho               |
| 📦 PyInstaller    | Empacotamento em executável `.exe`      |
| 🔑 python-dotenv  | Leitura segura de variáveis de ambiente |

---

## 🗺 Roadmap

- [ ] Interface gráfica (GUI)
- [ ] Suporte a mais modelos de IA no renomeador
- [ ] Detecção automática da posição da marca d'água
- [ ] Exportação de relatório em PDF após processamento

---

## 📄 Licença

Este projeto está licenciado sob a licença **MIT**.  
Desenvolvido com 💜 por **Vítor Gomes**.
