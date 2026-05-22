import base64
import requests
import os
import shutil
from config import OPENROUTER_URL, MODELO_VISAO

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def solicitar_nome_ia(image_path: str, api_key: str, prompt_text: str) -> str:
    base64_image = encode_image(image_path)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Tratamento da extensão do mimetype para vision
    file_ext = os.path.splitext(image_path)[1][1:].lower()
    if file_ext == 'jpg': 
        file_ext = 'jpeg'
    mime_type = f"image/{file_ext}"

    image_url = f"data:{mime_type};base64,{base64_image}"

    payload = {
        "model": MODELO_VISAO,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    }
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            sugestao = data["choices"][0]["message"]["content"]
            # Limpeza caso a IA traga aspas envolto da palavra (bastante comum)
            sugestao = sugestao.strip().replace('"', '').replace("'", "")
            return sugestao
        else:
            raise Exception("Formato de resposta inesperado da API.")
    else:
        raise Exception(f"Erro na API OpenRouter ({response.status_code}): {response.text}")

def renomear_arquivo_localmente(caminho_antigo: str, novo_nome_base: str) -> str:
    diretorio = os.path.dirname(caminho_antigo)
    extensao = os.path.splitext(caminho_antigo)[1]
    
    novo_nome_completo = f"{novo_nome_base}{extensao}"
    novo_caminho = os.path.join(diretorio, novo_nome_completo)
    
    contador = 1
    # Verifica duplicidade para evitar substituir acidentalmente fotos similares
    while os.path.exists(novo_caminho):
        novo_nome_completo = f"{novo_nome_base}_{contador}{extensao}"
        novo_caminho = os.path.join(diretorio, novo_nome_completo)
        contador += 1
        
    shutil.move(caminho_antigo, novo_caminho)
    return novo_caminho
