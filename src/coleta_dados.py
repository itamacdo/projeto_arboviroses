import requests
import pandas as pd
import os

def buscar_dados_arboviroses(municipio_ibge, ano_inicio, ano_f):
    if not os.path.exists('data'):
        os.makedirs('data')
        
    doencas = ['dengue', 'zika', 'chikungunya']
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for doenca in doencas:
        url = f"https://info.dengue.mat.br/api/alertcity?geocode={municipio_ibge}&disease={doenca}&format=csv&ew_start=1&ey_start={ano_inicio}&ew_end=52&ey_end={ano_f}"
        print(f"Buscando dados de {doenca}...")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open(f'data/{doenca}_{municipio_ibge}.csv', 'wb') as f:
                    f.write(response.content)
                print(f"✅ {doenca.capitalize()} salvo!")
        except Exception as e:
            print(f"❌ Erro em {doenca}: {e}")

if __name__ == "__main__":
    buscar_dados_arboviroses(2301901, 2023, 2026)