import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# Extensões de imagem aceitas
EXTENSOES_ACEITAS = [".jpg", ".jpeg", ".png", ".webp"]

# Configurações do OpenRouter
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
# O GPT-4o suporta vision.
MODELO_VISAO = os.getenv("MODELO_VISAO", "openai/gpt-4o")

# Prompts guardados na configuração
PROMPT_NOME_CRIATIVO = """Analise esta imagem de um produto novo (tábua de corte em resina) e gere um nome curto, impactante e marketeiro que transmita valor e qualidade. O nome deve ter no máximo 3-4 palavras, sem acentos, com underscores no lugar de espaços e deve ser em Português PT-BR.

Responda APENAS com o nome, nada mais. Exemplo: "Vida Marítima"
"""

PROMPT_NOME_DESCRITIVO = """Analise esta imagem de um produto novo (tábua de corte em resina) e gere um nome descritivo e técnico que detalhe as características visuais do produto. O nome deve ser detalhado (5-7 palavras), sem acentos, com underscores no lugar de espaços e deve ser em Português PT-BR.

Responda APENAS com o nome, nada mais. Exemplo: "Tabua_Resina_Marmoreizada_Efeito_Agua_Luxo_Premium"
"""
