import os
import django
import pandas as pd
import numpy as np
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import EstatisticaViolencia

def format_text(text):
    if pd.isna(text):
        return "Não Informado"
    t = str(text).upper()
    if 'FEMINICDIO' in t or 'FEMINICDIO' in t:
        return 'Feminicídio'
    if 'HOMICDIO' in t or 'HOMICDIO' in t:
        return 'Homicídio'
    if 'AGRESSAO' in t or 'AGRESSO' in t:
        return 'Agressão Física'
    if 'AMEACA' in t or 'AMEAA' in t:
        return 'Ameaça'
    if 'ESTUPRO' in t:
        return 'Estupro'
    return t.title()

def get_age_group(age):
    try:
        age = float(age)
        if age < 18: return '0-17'
        if age <= 25: return '18-25'
        if age <= 35: return '26-35'
        if age <= 45: return '36-45'
        if age <= 55: return '46-55'
        return '56+'
    except:
        return 'Não Informada'

def get_race(race):
    if pd.isna(race) or race == 'NI':
        return 'Não Informada'
    return str(race).title()

def run_import():
    file_path = 'base/DADOS_VIOLENCIA_MULHER.xlsx'
    print("Lendo arquivo Excel...")
    df = pd.read_excel(file_path)
    
    print("Apagando dados antigos...")
    EstatisticaViolencia.objects.all().delete()
    
    print("Preparando registros...")
    records = []
    
    for index, row in df.iterrows():
        # Handle date
        ano = 0
        mes = 0
        date_val = row['data_fato']
        if pd.notnull(date_val):
            if isinstance(date_val, datetime.datetime):
                ano = date_val.year
                mes = date_val.month
            else:
                try:
                    dt = pd.to_datetime(date_val)
                    ano = dt.year
                    mes = dt.month
                except:
                    pass
        
        # Determine crime type correctly based on user screenshot/data
        # Actually in the Excel, 'natureza' has the crime.
        crime = format_text(row['natureza'])
        
        # If year is 0, let's just assume a default or skip
        if ano == 0:
            ano = 2023 # fallback
            
        mun = str(row['municipio_fato']).title() if pd.notnull(row['municipio_fato']) else "Não Informado"
        
        record = EstatisticaViolencia(
            municipio=mun,
            tipo_crime=crime,
            ano=ano,
            mes=mes,
            quantidade=1,  # Each row is 1 occurrence
            perfil_vitima_idade=get_age_group(row['idade']),
            perfil_vitima_raca=get_race(row['cor_raca'])
        )
        records.append(record)
        
    print(f"Inserindo {len(records)} registros reais no banco de dados...")
    EstatisticaViolencia.objects.bulk_create(records)
    print("Importação concluída com sucesso!")

if __name__ == '__main__':
    run_import()
