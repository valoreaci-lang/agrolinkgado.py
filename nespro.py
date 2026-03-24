import requests
from bs4 import BeautifulSoup

# --- SEUS DADOS ---
TOKEN = "8588052322:AAEraKnzeDWUvgGKSzYgX3SwEpYsf1Kteqo"
CHAT_ID = "7974959962"

def buscar_nespro():
    url = "https://www.ufrgs.br/nespro/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table')
        if not tabela: return "⚠️ Tabela de preços não encontrada no site."
        
        linhas = tabela.find_all('tr')
        msg = "🐂 *COTAÇÃO NESPRO - RS*\n\n"
        # Pega as primeiras 6 linhas da tabela de preços
        for linha in linhas[:7]:
            colunas = [c.text.strip() for c in linha.find_all('td')]
            if len(colunas) >= 2:
                msg += f"• *{colunas[0]}:* {colunas[1]}\n"
        return msg
    except Exception as e:
        return f"❌ Erro ao buscar dados: {e}"

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})

if __name__ == "__main__":
    enviar_telegram(buscar_nespro())
