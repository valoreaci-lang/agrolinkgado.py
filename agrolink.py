import requests
from bs4 import BeautifulSoup

# SEUS DADOS (Pode usar os mesmos do Nespro ou criar um novo no BotFather)
TOKEN = "8588052322:AAEraKnzeDWUvgGKSzYgX3SwEpYsf1Kteqo"
CHAT_ID = "7974959962"

def buscar_agrolink():
    url = "https://www.agrolink.com.br/cotacoes/carnes/bovinos/"
    
    # O "disfarce" para o site não bloquear o robô
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # O Agrolink organiza os dados em listas ou tabelas. 
        # Vamos pegar as linhas da tabela principal:
        tabela = soup.find('table', {'class': 'table-cotacoes'})
        if not tabela: return "⚠️ Não consegui ler a tabela do Agrolink hoje."
        
        linhas = tabela.find_all('tr')
        msg = "🥩 *AGROLINK - COTAÇÕES BOVINOS*\n\n"
        
        # Pegamos as 5 primeiras linhas (Boi Gordo, Vaca, etc.)
        for linha in linhas[1:6]: 
            cols = linha.find_all('td')
            if len(cols) >= 2:
                produto = cols[0].text.strip()
                preco = cols[1].text.strip()
                variacao = cols[2].text.strip() if len(cols) > 2 else ""
                msg += f"• *{produto}:* {preco} ({variacao})\n"
                
        return msg
    except Exception as e:
        return f"❌ Erro no Agrolink: {e}"

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})

if __name__ == "__main__":
    enviar_telegram(buscar_agrolink())
