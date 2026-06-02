import pandas as pd
import re

# Deu muito trabalho! O arquivo bruto estava muito bagunçado
df = pd.read_excel("Historico bruto.xlsx")

df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

df['Data'] = df['Data'].apply(lambda x: x.replace(year=2026) if pd.notnull(x) else x)

df = df.sort_values(by='Data').reset_index(drop=True)

df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')

def tratar_duracao(valor):
    if pd.isna(valor):
        return 0
    
    texto = str(valor).strip().lower()
    
    horas = 0
    match_h = re.search(r'(\d+)\s*h', texto)
    if match_h:
        horas = int(match_h.group(1))
    
    if 'h' in texto:
        parte = texto.split('h')[1]
    else:
        parte = texto
    
    minutos = 0
    match_m = re.search(r'(\d+)', parte)
    if match_m:
        minutos = int(match_m.group(1))
    
    return horas * 60 + minutos

df['Duracao_Min'] = df['Duração'].apply(tratar_duracao)

df = df.drop_duplicates()

df.to_excel("Produto final.xlsx", index=False)

print("Correção concluída!")
