import requests
from bs4 import BeautifulSoup

# SEUS DADOS
TOKEN = "8588052322:AAEraKnzeDWUvgGKSzYgX3SwEpYsf1Kteqo"
CHAT_ID = "7974959962"

def buscar_agrolink():
    # Link focado no Rio Grande do Sul
    url = "https://www.agrolink.com.br/cotacoes/carnes/bovinos/rs/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8' # Garante que os acentos fiquem certos
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tentativa 1: Buscar pela classe padrão do Agrolink
        tabela = soup.find('table', {'class': 'table-cotacoes'})
        
        # Tentativa 2: Se não achar, busca qualquer tabela na página
        if not tabela:
            tabela = soup.find('table')

        if not tabela:
            return "⚠️ O site do Agrolink mudou o formato e não encontrei a tabela."
        
        linhas = tabela.find_all('tr')
        msg = "🥩 *AGROLINK - RS (BOVINOS)*\n\n"
        
        encontrou_dados = False
        for linha in linhas[1:8]: # Pega as primeiras linhas de dados
            cols = linha.find_all('td')
            if len(cols) >= 2:
                produto = cols[0].text.strip()
                preco = cols[1].text.strip()
                msg += f"• *{produto}:* {preco}\n"
                encontrou_dados = True
                
        if not encontrou_dados:
            return "⚠️ Encontrei a tabela, mas ela parece estar vazia hoje."
            
        return msg

    except Exception as e:
        return f"❌ Erro ao acessar Agrolink: {e}"

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

if __name__ == "__main__":
    enviar_telegram(buscar_agrolink())
